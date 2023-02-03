from odoo import fields, models


class EstatePropertyTag(models.Model):
	_name = "estate.property.tag"
	_description = "estate property tag"
	_order = "name"
	_sql_constraints = [
		('check_name_unique', 'unique(name)',
		 'The tag name should be unique!')
	]

	name = fields.Char(string="Name", required=True)
	color = fields.Integer(string="Color")

