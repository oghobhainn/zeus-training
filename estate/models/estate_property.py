from datetime import timedelta  #, relativedelta

from odoo import api, fields, models, exceptions, tools, _

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    _order = "id desc"

    _sql_constraints = [
        ('estate_property_check_expected_price', 'CHECK(expected_price > 0)',
                'The expected price must be strictly positive.'),
        ('estate_property_check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be positive.'),
    ]

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    data_availability = fields.Date('Available From', copy=False,
                                    default=lambda self: fields.Datetime.today() + timedelta(days=90))
                                    #default=fields.Date.today() + relativedelta(months=3)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False, compute='_compute_selling_price')
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades', default=2)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'),
                                            ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string='State', selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('cancel', 'Canceled')],
                             default='new', required=True, copy=False)
    property_type = fields.Many2one('estate.property.type', string='Property Type')
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tags_id = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(compute='_compute_total_area', string='Total Area (sqm)', readonly=True)
    best_price = fields.Float(string='Best Offer', readonly=True, compute='_compute_highest_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_highest_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(offer.price for offer in record.offer_ids)
            else:
                record.best_price = 0

    @api.depends('offer_ids.status')
    def _compute_selling_price(self):
        self.selling_price = 0
        self.buyer = None
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                self.selling_price = offer.price
                self.buyer = offer.partner_id

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlike_if_state_not_new_and_not_cancel(self):
        if not self.state in ['new','cancel']:
            raise exceptions.UserError(_('It is not allowed to delete the record!'))

    def action_set_sold(self):
        message = 'You can\'t set a cancelled property to sold!'
        if self.state == 'cancel':
            raise exceptions.UserError(_(message))

        self.state = 'sold'
        return True

    def action_set_cancel(self):
        message = 'You can\'t set a sold property to cancelled!'
        if self.state == 'sold':
            raise exceptions.UserError(_(message))

        self.state = 'cancel'
        return True