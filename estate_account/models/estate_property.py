# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, Command
class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_to_sold(self):
        #moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)

        self.env['account.move'].create(
            {
                'move_type': 'out_invoice',
                'partner_id': self.buyer_id.id,
                'journal_id': self.env['account.journal'].search([('id',"=",1)]).id,
                "invoice_line_ids": [
                    Command.create({
                        "name" : self.name,
                        "quantity": 1,
                        "price_unit": self.selling_price
                    }),
                    Command.create({
                        "name": 'Administrative fees',
                        "quantity": 1,
                        "price_unit": 100.00
                    })
                ],

            })
        return super().action_set_to_sold()