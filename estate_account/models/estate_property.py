from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        invoice_info = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                fields.Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': (self.selling_price * 0.06),
                }),
                fields.Command.create({
                    'name': 'administration',
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ]
        }

        self.env['account.move'].create(invoice_info)
        return super().action_set_sold()