from odoo import api, fields, models, exceptions, _

class ShoppingListDetail(models.Model):
    _name = "shopping.list.detail"
    _description = "Shopping List Detail"

    name = fields.Char('Product', required=True)
    in_bag = fields.Boolean('In Bag', copy=False)
    remark = fields.Char('Remark', copy=False)
    list_id = fields.Many2one('shopping.list', required=True, copy=False, ondelete='cascade')
    status_list = fields.Char(compute='_compute_get_status', string='Status List')
    user_created = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        #if self.env['shopping.list'].browse(self.list_id.id).state != 'new':
        #    raise exceptions.UserError(_("It is not allowed to add products when the state is not new"))
        return super().create(vals)

    def write(self, vals):
        #import ipdb;ipdb.set_trace()
        if 'in_bag' in vals:
            if (self.in_bag != vals['in_bag']) and (vals['in_bag']):
                self.env['shopping.list'].browse(self.list_id.id).state = 'in_progress'
            elif (self.in_bag != vals['in_bag']) and not (vals['in_bag']):
                if self.search_count([('in_bag', '=', True), ('id', '!=', self.id), ('list_id', '=', self.list_id.id)]) == 0:
                    self.env['shopping.list'].browse(self.list_id.id).state = 'new'

        return super().write(vals)

    def _compute_get_status(self):
        for record in self:
            #record.status_list = record.mapped('list_id.detail_ids.state')
            record.status_list = record.list_id.state

    def action_in_bag(self):
        for record in self:
            if record.in_bag:
                record.in_bag = False
            else:
                record.in_bag = True
