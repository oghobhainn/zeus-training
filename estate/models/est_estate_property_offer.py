# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class EstatePropertyOffer(models.Model):
    _name = "est.estates.property.offer"
    _description = "Estates Property Offer"

    price = fields.Float(default=0)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("est.estates.property", required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    _sql_constraints = [
        ('Check_price', 'CHECK(price > 0)',
         'The offer price should be greater than 0!')
    ]

    @api.constrains('price')
    def _check_price_against_expected_price(self):
        for record in self:
            expectedprice = self.property_id.expected_price
            if record.price < expectedprice:
                raise ValidationError(('hoi %s') % (expectedprice))

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date != 0:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date != 0:
                creationdate = datetime.date(record.create_date)
                deltadate = record.date_deadline - creationdate
                record.validity = deltadate.days

    def action_property_offer_accept(self):
        for record in self:
            record.status ='accepted'
        if self.search_count([('status', '=', 'accepted')]) > 1:
            raise ValidationError('Only 1 offer can be accepted!')

    def action_property_offer_refuse(self):
        for record in self:
            record.status = 'refused'