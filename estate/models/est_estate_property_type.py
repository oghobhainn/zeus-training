# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "est.estates.property.type"
    _description = "Estates Property type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('Check_unique_name', 'UNIQUE(name)',
         'Name must be unique!')
    ]