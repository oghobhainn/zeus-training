from odoo import api, fields, models, exceptions, _
from datetime import datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Properties Offer"
    _order = "price desc"
    _sql_constraints = [('check_price', 'CHECK (price > 0)', '''The offer price must be strictly positive.''')]

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
                                copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.model
    def create(self, vals):
        if self.search_count([('price', '>', vals['price']), ('property_id', '=', vals['property_id'])]) > 0:
            raise exceptions.UserError(_("The offer can't be lower then the existing offers"))

        self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        return super().create(vals)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            createdate = record.create_date
            if not createdate:
                createdate = fields.Date.today()

            record.date_deadline = fields.Date.add(createdate, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            createdate = record.create_date
            if not createdate:
                createdate = fields.Date.today()

            date_created = datetime.date(createdate)

            date_range = record.date_deadline - date_created
            record.validity = date_range.days

    @api.constrains('price')
    def check_selling_price(self):
        for record in self:
            expected_price = record.property_id.expected_price
            if (record.status == 'accepted') and ((0.9 * expected_price) > record.price):
                #if record.price != 0:
                #    if ((0.9 * expected_price) > record.price):
                raise exceptions.ValidationError(_("The offered price is to low!"))

    def action_accept(self):
        #import ipdb; ipdb.set_trace()
        if 'accepted' in self.mapped('property_id.offer_ids.status'):
            raise exceptions.ValidationError(_('Only 1 record can be accepted'))
        else:
            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'

    def action_refuse(self):
        self.status = 'refused'



