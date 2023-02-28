# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("est.estates.property", "salesman", string="Properties",
                                   domain=['|', ('state', '=', 'new'), ('state', '=', 'offer received')])
