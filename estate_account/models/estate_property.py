from odoo import models
from odoo import Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def set_estate_property_to_sold(self):
        invoice_vals_list = []

        invoice_vals = {
            "move_type": "out_invoice",
            "partner_id": self.buyer_id.id,
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": (self.selling_price * 0.06),
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100,
                }),
            ]
        }
        invoice_vals_list.append(invoice_vals)

        self.env['account.move'].create(invoice_vals_list)

        return super().set_estate_property_to_sold()
