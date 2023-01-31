from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        help="Status is used to define the status",
        copy=False)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property ID", required=True)

    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

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
