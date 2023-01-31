from odoo import fields, models


class EstatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "estate property type"

	name = fields.Char(string="Name", required=True)

	_sql_constraints = [
		('check_name_unique', 'unique(name)',
		 'The type name should be unique!')
	]