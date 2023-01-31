# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "est.estates.property.type"
    _description = "Estates Property type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('est.estates.property', 'type_id', string="Properties")
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many("est.estates.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute='_compute_offers_count')

    _sql_constraints = [
        ('Check_unique_name', 'UNIQUE(name)',
         'Name must be unique!')
    ]

    def _compute_offers_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)

    def open_property_type_offers(self):
        res = self.env.ref('estate.estate_model_offer_action').read()[0]
        res["domain"] = [('id', 'in', self.offer_ids.ids)]
        return res
