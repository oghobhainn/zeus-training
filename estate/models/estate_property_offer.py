from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        help="Status is used to define the status",
        copy=False)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today()
            if record.create_date:
                record.date_deadline = record.create_date

            record.date_deadline += relativedelta(days=record.validity)

    def _inverse_deadline(self):
        pass
        # self.date_deadline = self.date_deadline

    def set_offer_to_accepted(self):
        for propertyOffer in self:
            for offer in propertyOffer.property_id.offer_ids:
                if offer.status == "accepted":
                    raise UserError("Another offer was already accepted!")
            propertyOffer.property_id.selling_price = propertyOffer.price
            propertyOffer.property_id.buyer_id = propertyOffer.partner_id
            propertyOffer.status = "accepted"
        return True

    def set_offer_to_refused(self):
        for propertyOffer in self:
            propertyOffer.property_id.selling_price = 0
            propertyOffer.property_id.buyer_id = ''
            propertyOffer.status = "refused"
        return True

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive!')
    ]
