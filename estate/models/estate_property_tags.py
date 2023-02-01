from odoo import fields, models

class EstatePropertyTage(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Properties Tags"
    _order = "name"

    _sql_constraints = [
        ('name', 'unique (name)', """Only one value can be defined for each given tag!"""),
    ]

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')