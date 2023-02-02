# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.exceptions import ValidationError, UserError
from odoo import Command

class EstateProperty(models.Model):
    _inherit = "est.estates.property"

    invoice_ids = fields.One2many('account.move', "property_id", string='Invoices',
                                  copy=False, readonly=True)
    invoice_count = fields.Integer(compute='_compute_invoices_count')


    def _compute_invoices_count(self):
        for property in self:
            property.invoice_count = len(property.invoice_ids)

    def open_property_invoices(self):
        self.ensure_one()
        if self.invoice_ids:
            return {
                'name': 'Invoice created',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.move',
                'view_id': self.env.ref('account.view_move_form').ids,
                'target': 'current',
                'res_id': self.invoice_ids.id,
                }

    def action_property_sold(self):
        super().action_property_sold()

        # create invoice from estate property
        move = self.env['account.move'].create({'partner_id': self.buyer.id,
                                                'move_type': 'out_invoice',
                                                'line_ids': [
                                                    Command.create(
                                                        {
                                                            'name': self.name,
                                                            'quantity': 1,
                                                            'price_unit': self.selling_price / 100 * 6
                                                        }),
                                                    Command.create(
                                                        {
                                                            'name': 'Administrative Fees',
                                                            'quantity': 1,
                                                            'price_unit': 100
                                                        })
                                                    ]
                                                })

        move.property_id = self.id

        return super().action_property_sold()
