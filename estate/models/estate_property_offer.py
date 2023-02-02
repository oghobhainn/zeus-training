# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions, _
from datetime import datetime
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [('check_price', 'CHECK (price > 0)', 'The offer price must be positive.')]

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Estate Property', required=True)
    validity = fields.Integer('Validity', default='7')
    date_deadline = fields.Date(string='Date Deadline', compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        #print('Hello compute')
        for record in self:
            date_creation = record.create_date
            if not record.create_date:
                date_creation = fields.Date.today()

            record.date_deadline = fields.Date.add(date_creation, days=record.validity)

    @api.constrains('price', 'status')
    def check_percentage_price(self):
        message = 'The selling price must be 90% of the expected price'
        for record in self:
            if (record.status == 'accepted') and (record.price != None):
                    expectedprice = self.property_id.expected_price * 0.9
                    if record.price < expectedprice:
                        raise ValidationError(_(message))

    def _inverse_date_deadline(self):
        #print('Hello inverse')
        #import ipdb;
        #ipdb.set_trace()

        for record in self:
            date_creation = record.create_date
            if not record.create_date:
                date_creation = fields.Date.today()
            else:
                date_creation = record.create_date

            date_creation = datetime.date(record.create_date)
            deltadays = record.date_deadline - date_creation

            record.validity = deltadays.days

    def action_offer_accept(self):
        for record in self:
            if 'accepted' in record.mapped('property_id.offer_ids.status'):
                raise exceptions.ValidationError(_('Only one offer can be accepted!'))
            else:
                record.status = 'accepted'
                #record.property_id.buyer_id = record.partner_id

        return True

    def action_offer_refuse(self):
        for record in self:
            record.status = 'refused'
        return True