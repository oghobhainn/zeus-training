from odoo import fields, models

class EstatePropertyTage(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Properties Tags"

    name = fields.Char('Name', required=True)