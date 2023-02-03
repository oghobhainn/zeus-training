# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions, _
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    name = fields.Char(required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False,
                                    default=datetime.date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False, readonly=True, compute='_compute_selling_price')
    bedrooms = fields.Integer('Number of Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Garage ?')
    garden = fields.Boolean('Garden ?')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='General State',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new',
        required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area')
    best_price = fields.Float(compute='_compute_best_price', string='Best Price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        bestprice = 0
        for offer in self.offer_ids:
            bestprice = max(bestprice, offer.price)

        self.best_price = bestprice

    @api.depends('offer_ids')
    def _compute_selling_price(self):
        sellingprice = 0
        buyerid = None
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                sellingprice = offer.price
                buyerid = offer.partner_id

        self.selling_price = sellingprice
        self.buyer_id = buyerid

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = None
        #example
        #self.name = "Document for %s" % (self.partner_id.name)
        #self.description = "Default description for %s" % (self.partner_id.name)

    def action_sold(self):
        #example
        #for record in self:
        #    record.name = "Something"
        #return True
        message = 'You can\'t cancel a sold property!'
        for property in self:
            if property.state == 'canceled':
                raise exceptions.UserError(_(message))
            self.state = 'sold'
        return  True

    def action_cancel(self):
        message = 'You can\'t cancel a sold property!'
        for property in self:
            if property.state == 'sold':
                raise exceptions.UserError(_(message))
            self.state = 'canceled'
        return  True