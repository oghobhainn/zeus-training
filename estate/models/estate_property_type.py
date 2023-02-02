from odoo import api, fields, models


class EstatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "estate property type"
	_order = "name"
	_sql_constraints = [
		('check_name_unique', 'unique(name)',
		 'The type name should be unique!')
	]

	name = fields.Char(string="Name", required=True)
	property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
	sequence = fields.Integer(string="Sequence")
	offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
	offer_count = fields.Integer(String="Offer Count", compute="_compute_offer_count")

	@api.depends("offer_ids")
	def _compute_offer_count(self):
		for estate_property_type in self:
			estate_property_type.offer_count = len(estate_property_type.offer_ids)
