from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Estate Property Type Name", required=True)
    sequence = fields.Integer("Sequence", default=1)

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count  = 0
            for offer in property_type.offer_ids:
                property_type.offer_count += 1
