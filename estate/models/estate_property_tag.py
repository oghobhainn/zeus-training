# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property tag"
    _order = "name"
    _sql_constraints = [
        ('check_unique_tag', 'unique(name)',
         'The tag must be unique')
    ]

    name = fields.Char(required=True)
    color = fields.Integer()






