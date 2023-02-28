# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, _, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class EstatePropertyOffer(models.Model):
    _name = "est.estates.property.offer"
    _description = "Estates Property Offer"
    _order = "price desc"

    price = fields.Float(default=0)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("est.estates.property", required=True, ondelete='cascade')
    property_type_id = fields.Many2one(related='property_id.type_id')
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline', default=fields.Date.add(fields.Date.today(), days=7))

    _sql_constraints = [
        ('Check_price', 'CHECK(price > 0)',
         'The offer price should be greater than 0!')
    ]

    @api.constrains('price')
    def _check_price_against_expected_price(self):
        for record in self:
            expectedprice = self.property_id.expected_price / 100 * 90
            if record.price < expectedprice:
                raise ValidationError(_('The selling price should be at least %s', expectedprice))

    @api.model
    def write(self, vals):
        self._check_price(vals)
        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get('property_id'):
            property = self.env['est.estates.property'].browse(vals['property_id'])
            property.write({'state': 'offer received'})

        self._check_price(vals)
        return super().create(vals)
    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date != 0:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _check_price(self, vals):
        if vals.get('property_id'):
            id_of_current_property = vals['property_id']
        else:
            id_of_current_property = self.property_id.id

        if vals.get('price'):
            if self.search_count([('price', '>', vals['price']), ('property_id', '=', id_of_current_property)]) > 0:
                raise UserError(_('You cannot create an offer with a price lower than an existing offer!'))

        return vals

    def _inverse_deadline(self):
        for record in self:
            if record.create_date != 0:
                creationdate = datetime.date(record.create_date)
                deltadate = record.date_deadline - creationdate
                record.validity = deltadate.days

    def action_property_offer_accept(self):
        if self.search_count([('status', '=', 'accepted'), ('property_id', '=', self.property_id.id)]) > 0:
            raise ValidationError(_('Only 1 offer can be accepted!'))

        for record in self:
            record.status = 'accepted'

    def action_property_offer_refuse(self):
        for record in self:
            record.status = 'refused'