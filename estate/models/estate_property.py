from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError

class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "estate property"

	name = fields.Char(string="Title", required=True)
	description = fields.Text(string="Description")
	postcode = fields.Char(string="Postcode")
	date_availability = fields.Date(string="Available From",
									copy=False,
									default=lambda self: fields.Datetime.today() + timedelta(days=90)
									)
	expected_price = fields.Float(string="Expected Price", required=True)
	selling_price = fields.Float(string="Selling Price", readonly=True, copy=False, compute="_compute_selling_price")
	bedrooms = fields.Integer(string="Bedrooms", default=2)
	living_area = fields.Integer(string="Living Area (sqm)")
	facades = fields.Integer(string="Facades")
	garage = fields.Boolean(string="Garage")
	garden = fields.Boolean(string="Garden")
	garden_area = fields.Integer(string="Garden Area (sqm)")
	garden_orientation = fields.Selection(
		string='Garden orientation',
		selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
	active = fields.Boolean(string="Active", default=True)
	state = fields.Selection(
		string='State',
		selection=[
			('new', 'New'),
			('offer received', 'Offer Received'),
			('offer accepted', 'Offer Accepted'),
			('sold', 'Sold'),
			('canceled', 'Canceled')],
		required=True,
		default='new',
		copy=False
	)
	property_type_id = fields.Many2one("estate.property.type", string="Property Type")
	buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
	seller_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
	tag_ids = fields.Many2many("estate.property.tag", string="Tags")
	offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
	total_area = fields.Float(String="Total Area", compute="_compute_total_area")
	best_price = fields.Float(String="Best Offer", compute="_compute_best_offer")

	_sql_constraints = [
		('check_expected_price2', 'CHECK(expected_price > 0)',
		 'The expected price should be strictly positive!'),
		('check_selling_price2', 'CHECK(selling_price >= 0)',
		 'The selling price should not be negative!')
	]

	@api.depends("living_area", "garden_area")
	def _compute_total_area(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area


	@api.depends("offer_ids.price")
	def _compute_best_offer(self):
		self.best_price = 0
		for record in self:
			# record.best_price = max(self.env['estate.property.offer'].search([]).mapped('price'))
			if record.offer_ids:
				record.best_price = max(offer.price for offer in record.offer_ids)

	@api.depends("offer_ids.status")
	def _compute_selling_price(self):
		for record in self:
			record.reset_selling_price()
			accepted_offer = record.env['estate.property.offer'].search([('status', '=', 'accepted'),
																   ('property_id', '=', record.name)])
			if accepted_offer:
					record.selling_price = accepted_offer.price
					record.buyer_id = accepted_offer.partner_id

	@api.onchange("garden")
	def _onchange_garden(self):
		if self.garden:
			self.garden_area = 10
			self.garden_orientation = 'north'
		else:
			self.garden_area = 0
			self.garden_orientation = ''

	# actions
	def action_sold(self):
		if self.state == 'canceled':
			raise ValidationError(("A %s property cannot be %s") % (self.state, 'sold'))
		else:
			self.state = 'sold'

	def action_cancel(self):
		if self.state == 'sold':
			raise ValidationError(("An %s property cannot be %s") % (self.state, 'canceled'))
		else:
			self.state = 'canceled'


	def reset_selling_price(self):
		self.selling_price = 0
		self.buyer_id = ''

