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
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    @api.depends('validity')
    def _compute_date_deadline(self):
        #print('Hello compute')
        for offer in self:
            date_creation = offer.create_date
            if not offer.create_date:
                date_creation = fields.Date.today()

            offer.date_deadline = fields.Date.add(date_creation, days=offer.validity)

    @api.constrains('price', 'status')
    def check_percentage_price(self):
        message = 'The selling price must be 90% of the expected price'
        for offer in self:
            if (offer.status == 'accepted') and (offer.price != None):
                    expectedprice = self.property_id.expected_price * 0.9
                    if offer.price < expectedprice:
                        raise ValidationError(_(message))

    def _inverse_date_deadline(self):
        #print('Hello inverse')
        #import ipdb;
        #ipdb.set_trace()

        for offer in self:
            date_creation = offer.create_date
            if not offer.create_date:
                date_creation = fields.Date.today()
            else:
                date_creation = offer.create_date

            date_creation = datetime.date(offer.create_date)
            deltadays = offer.date_deadline - date_creation

            offer.validity = deltadays.days

    def action_offer_accept(self):
        for offer in self:
            if 'accepted' in offer.mapped('property_id.offer_ids.status'):
                raise exceptions.ValidationError(_('Only one offer can be accepted!'))
            else:
                offer.status = 'accepted'
                offer.property_id.state = 'offer received'
                #record.property_id.buyer_id = record.partner_id

        return True

    def action_offer_refuse(self):
        for offer in self:
            offer.status = 'refused'

        return True