# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'Selling price must be positive')
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Datetime.add(fields.Datetime.now(),months=3),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False,compute="_compute_selling_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
        help="test")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'),
                   ('Sold', 'Sold'), ('Canceled', 'Canceled')],
        default='New',
        copy=False,
        )
    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one("res.users", string="Salesman", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer",compute="_compute_buyer_id")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    test_odoosh = fields.Char()

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for property in self:
            property.best_price = 0
            for offer in property.offer_ids:
                if property.best_price < offer.price :
                    property.best_price = offer.price

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden :
                record.garden_area = 10
                record.garden_orientation = 'North'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    @api.depends("offer_ids.status")
    def _compute_selling_price(self):
        self.selling_price = 0;
        for offer in self.offer_ids:
            if offer.status == 'Accepted' :
              self.selling_price = offer.price

    @api.depends("offer_ids.status")
    def _compute_buyer_id(self):
        self.buyer_id = '';
        for offer in self.offer_ids:
            if offer.status == 'Accepted':
               self.buyer_id = offer.partner_id

    def action_cancel_property(self):
        for property in self:
            if property.state == "Sold":
                raise UserError('Property already sold : cannot be canceled !')
            property.state = "Canceled"

    def action_set_to_sold(self):
        for property in self:
            if property.state == "Canceled":
                raise UserError('Property already canceled : cannot be sold !')
            property.state = "Sold"

    @api.ondelete(at_uninstall=False)
    def check_status_on_delete(self):
        for property in self:
            if not (property.state in ('New','Canceled')):
                raise ValidationError("offer with status New or Canceled cannot be deleted")

