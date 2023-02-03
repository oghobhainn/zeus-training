# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    _sql_constraints = [
        ('Check_unique_name', 'UNIQUE(name)',
         'Name must be unique!')
    ]
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help='Used to order stages. Lower is better.')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_count_offers')

    @api.depends('offer_ids')
    def _compute_count_offers(self):
        for property_type in self:
            #property_types_count = 0
            #for property_type_offer in property_type.offer_ids:
            #    property_types_count += 1
            #property_type.offer_count = property_types_count

            property_type.offer_count = len(property_type.offer_ids)