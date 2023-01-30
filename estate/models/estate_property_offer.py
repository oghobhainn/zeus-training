from odoo import fields, models


class EstatePropertyOffer(models.Model):
	_name = "estate.property.offer"
	_description = "estate property offer"

	price = fields.Float(string="Price")
	status = fields.Selection(
		string="Status",
		selection=[('accepted','Accepted'),('refused','Refused')]
	)