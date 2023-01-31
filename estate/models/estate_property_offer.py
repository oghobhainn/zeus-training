# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')]
        )

    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property")

    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")


    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self :
            record.date_deadline = fields.Datetime.add(fields.Datetime.now(), days=record.validity)
            if record.create_date :
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)
    def _inverse_deadline(self):
        pass







