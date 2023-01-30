from odoo import fields, models

class EstatePropertyTage(models.Model):
    _name = "estate.property.tage"
    _description = "Estate Properties Tage"

    name = fields.Char('Name', required=True)