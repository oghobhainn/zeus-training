from odoo import Command, fields, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                            'name': self.name,
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06
                        }),
                    Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1,
                            'price_unit': 100.00                                                             })
                        ]
            }
        )
        return super().action_sold()