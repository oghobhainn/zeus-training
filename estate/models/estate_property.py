from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property App"
    _order = "id desc"

    name= fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        help="Defines the direction in which the garden in oriented")

    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")],
        default="new",
        help="Choose the state of the Offer")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)

    tag_ids = fields.Many2many("estate.property.tag")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area")

    best_price = fields.Float(compute="_calculate_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids")
    def _calculate_best_price(self):
        self.best_price = 0
        for offers in self.offer_ids:
            if self.best_price < offers.price:
               self.best_price = offers.price

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = "north"
            else:
                property.garden_area = 0
                property.garden_orientation = ""

    def set_estate_property_to_sold(self):
        for property in self:
            if property.state == "canceled":
                raise UserError("Canceled properties cannot be sold!")
            else:
                property.state = "sold"
        return True

    def set_estate_property_to_canceled(self):
        for property in self:
            if property.state == "sold":
                raise UserError("Sold properties cannot be canceled!")
            else:
                property.state = "canceled"
        return True

    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise ValidationError("Selling Price cannot be lower than 90% of the Expected Price!")

    @api.ondelete(at_uninstall=False)
    def check_status_on_delete(self):
        for property in self:
            if (property.state != "new") and (property.state != "canceled"):
                raise UserError("Only new or canceled properties can be deleted!")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive!'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive!')
    ]

