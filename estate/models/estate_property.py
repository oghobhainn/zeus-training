from datetime import timedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    data_availability = fields.Date('Available From', copy=False,
                                    default=lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades', default=2)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'),
                                            ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string='State', selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('cancel', 'Canceled')],
                             default='new', required=True, copy=False)
    property_type = fields.Many2one('estate.property.type', string='Property Type')
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tags_id = fields.Many2many('estate.property.tage', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')