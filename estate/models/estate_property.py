# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Datetime.add(fields.Datetime.now(),months=3),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
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
        selection=[('New', 'New'), ('Offer', 'Offer'), ('Received', 'Received'),
                   ('Offer Accetped', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')],
        default='New',
        copy=False
        )





