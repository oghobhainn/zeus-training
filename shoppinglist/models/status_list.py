from odoo import api, fields, models, exceptions, _

class StatusList(models.Model):
    _name = "status.list"
    _description = "Status List"

    _sql_constraints = [
        ('name', 'unique (name)', """Only one value can be defined for each given type!"""),
    ]

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
    sl_ids = fields.One2many('shopping.list', 'status_name')