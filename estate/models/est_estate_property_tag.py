# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "est.estates.property.tag"
    _description = "Estates Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('Check_unique_name', 'UNIQUE(name)',
         'Name must be unique!')
    ]