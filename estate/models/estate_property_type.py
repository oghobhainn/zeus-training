from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Properties Type"
    _order = "sequence, name"

    _sql_constraints = [
        ('name', 'unique (name)', """Only one value can be defined for each given type!"""),
    ]

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Counted Offers')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_open_offers(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("estate.estate_property_offer_action")
        action['domain'] = [('id', 'in', self.offer_ids.ids)]
        return action

