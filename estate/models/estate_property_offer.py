from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError, UserError

class EstatePropertyOffer(models.Model):
	_name = "estate.property.offer"
	_description = "estate property offer"
	_order = "price desc"
	_sql_constraints = [
		('check_offer_price', 'CHECK(price > 0)',
		 'The offer price should be strictly positive!')
	]

	price = fields.Float(string="Price")
	status = fields.Selection(
		string="Status",
		selection=[('accepted','Accepted'),('refused','Refused')]
	)
	partner_id = fields.Many2one("res.partner", String="Partner", required=True)
	property_id = fields.Many2one("estate.property", String="Property", required=True)
	validity = fields.Integer(String="Validity (days)", default=7)
	date_deadline = fields.Date(String="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
	property_type_id = fields.Many2one("estate.property.type", String="Property Type", compute="_compute_property_type", store=True)

	@api.model
	def create(self, vals):
		res = super().create(vals)
		# raise UserError(res.property_id)
		max_offer = max(self.env['estate.property.offer'].search([('property_id', '=', res.property_id.id)]).mapped('price'))
		if res.price < max_offer:
			raise UserError(f'The offer must be higher than {max_offer:,.2f} Euro.')

		return res

	@api.depends("property_id.property_type_id")
	def _compute_property_type(self):
		for estate_property_offer in self:
			estate_property_offer.property_type_id = estate_property_offer.property_id.property_type_id

	@api.constrains("price", "status")
	def _check_price(self):
		for estate_property_offer in self:
			expected_price = 0.9 * self.property_id.expected_price
			if (self.status == 'accepted') and (self.price < expected_price):
				raise ValidationError(f'Offer price should not be lower than {expected_price:,.2f} Euro.')

	@api.depends("validity")
	def _compute_deadline(self):
		for estate_property_offer in self:
			if estate_property_offer.create_date:
				# record.date_deadline = record.create_date + timedelta(days=record.validity)
				estate_property_offer.date_deadline = fields.Date.add(estate_property_offer.create_date, days=estate_property_offer.validity)
			else:
				estate_property_offer.date_deadline = fields.Date.add(fields.Datetime.today(), days=estate_property_offer.validity)

	def _inverse_deadline(self):
		for estate_property_offer in self:
			if estate_property_offer.create_date:
				date_created = datetime.date(estate_property_offer.create_date)
				date_range = estate_property_offer.date_deadline - date_created
				estate_property_offer.validity = date_range.days

	def action_accept(self):
		if self.search_count([('status', '=', 'accepted'), ('property_id', '=', self.property_id.name)]) > 0:
			raise ValidationError('Only one offer can be accepted for a given property!')

		self.status = 'accepted'

	def action_refuse(self):
		self.status = 'refused'

