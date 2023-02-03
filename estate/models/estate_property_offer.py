# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)',
         'Offer price must be positive')
    ]

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')]
        )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property")
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related = "property_id.property_type_id")

    @api.constrains('price','status')
    def _check_selling_price(self):
        for offer in self:
            if offer.status == 'Accepted' :
                acceptable_price = (offer.property_id.expected_price * 90 / 100)
                if (offer.price > 0) and (offer.price < acceptable_price):
                    raise ValidationError("The selling price cannot be lower then 90% of the expected price")

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self :
            record.date_deadline = fields.Datetime.add(fields.Datetime.now(), days=record.validity)
            if record.create_date :
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)

    def _inverse_deadline(self):
        pass

    def action_accept_offer(self):
        for offer in self:
            if 'Accepted' in offer.mapped("property_id.offer_ids.status"):
                raise UserError('Only one offer can be accepted')
            else:
                offer.status = "Accepted"

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "Refused"

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        if property.state == 'New':
            property.state = 'Offer Received'
        offer_price = vals['price']
        for offer in property.offer_ids :
            if offer_price < offer.price :
               error_message = str('Offer price must be higher then {}' + format(offer.price))
               raise ValidationError(error_message)

        return super().create(vals)



