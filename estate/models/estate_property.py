from odoo import fields, models
from datetime import timedelta

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
	selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
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





