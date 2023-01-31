from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Properties Type"
    _order = "sequence, name"

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type')
    sequence = fields.Integer('Sequence', default=1)

    _sql_constraints = [
        ('name', 'unique (name)', """Only one value can be defined for each given type!"""),
    ]