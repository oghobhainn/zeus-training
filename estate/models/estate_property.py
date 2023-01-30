from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    data_availability = fields.Date('Data Available')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms', default=1)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades', default=2)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'),
                                            ('south', 'South'), ('east', 'East'), ('west', 'West')])

