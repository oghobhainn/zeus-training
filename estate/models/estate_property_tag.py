from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char("Estate Property Tag Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ('check_tag_name_unique', 'UNIQUE(name)', 'Property Tag name must be unique!')
    ]
