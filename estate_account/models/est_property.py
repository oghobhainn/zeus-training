# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.exceptions import ValidationError, UserError
from odoo import Command

class EstateProperty(models.Model):
    _inherit = "est.estates.property"

    def action_property_sold(self):
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
        return super().action_property_sold()
