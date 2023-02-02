# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_id = fields.Many2one('est.estates.property', 'invoice_id', readonly=True, copy=False)
