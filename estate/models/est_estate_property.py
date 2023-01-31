# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = "est.estates.property"
    _description = "Estates Property"
    _order = "id desc"

    name = fields.Char('Title', required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', copy=False,
                                    default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, compute='_compute_selling_price')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new')
    type_id = fields.Many2one("est.estates.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False, readonly=True)
    tag_ids = fields.Many2many("est.estates.property.tag", string="Tags")
    offer_ids = fields.One2many("est.estates.property.offer", "property_id", string="Offers")
    total_area = fields.Integer('Total Area (sqm)', compute='_set_area', readonly=True)
    best_price = fields.Float(compute='_compute_best_price')

    _sql_constraints = [
        ('Check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be greater than 0!')
    ]
    _sql_constraints = [
        ('Check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be greater or equal to 0')
    ]
    # private functions

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_is_new_or_cancelled(self):
        if any(property.state not in ['new', 'cancelled'] for property in self):
            raise UserError('You cannot delete a property that is not new or cancelled!')

    @api.depends('living_area', 'garden_area')
    def _set_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        self.best_price = 0
        for offer in self.offer_ids:
            if self.best_price < offer.price:
                self.best_price = offer.price

    @api.depends('offer_ids.status')
    def _compute_selling_price(self):
        self.selling_price = 0
        self.buyer = self.env["res.partner"]
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                self.selling_price = offer.price
                self.buyer = offer.partner_id

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = ''
            self.garden_area = 0

    # public functions

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise ValidationError(("An Estate Property that is %s can not be %s") % (record.state,'sold'))
            else:
                record.state ='sold'

    def action_property_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise ValidationError(("An Estate Property that is %s can not be %s") % (record.state, 'cancelled'))
            else:
                record.state = 'cancelled'