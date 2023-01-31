from odoo import fields, models

class EstatePropertyTage(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Properties Tags"
    _order = "name"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('name', 'unique (name)', """Only one value can be defined for each given tag!"""),
    ]