import copy

from odoo import api, fields, models, exceptions, _

class ShoppingList(models.Model):
    _name = "shopping.list"
    _description = "Shopping List"

    name = fields.Char('Title', required=True)
    date_list = fields.Date('Date Created', copy=False, default=fields.Date.today(), readonly=True)
    state = fields.Selection(selection=[('new', 'New'), ('in_progress', 'In Progress'), ('on_hold', 'On Hold'),
                                                    ('finished', 'Finished'), ('cancel', 'Cancelled')],
                             default='new', required=True, copy=False, string='State')
    status_name = fields.Many2one('status.list', string='Status', default='New', compute='_compute_status', store=True)
    detail_ids = fields.One2many('shopping.list.detail', 'list_id', string='Detail', copy=False, ondelete='cascade')
    active = fields.Boolean('Active', default=True)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        vals = self.with_context(active_test=False).copy_data(default)[0]
        vals['name'] = 'Duplicated of ' + self.name
        record_copy = self.create(vals)
        self.with_context(from_copy_translation=True).copy_translations(record_copy, excluded=default or ())

        self.create_detail_lines(record_copy.id, False)

        return record_copy

    @api.depends('state')
    def _compute_status(self):
        for record in self:
            record.status_name = self.env['status.list'].search([('name', 'ilike', record.state)])

    def action_set_finished(self):
        for record in self:
            if record.state == 'cancel':
                raise exceptions.UserError(_('You can not finish a list that is cancelled'))

            record.state = 'finished'
            copy_record = record

            if record.check_products_not_in_bag():
                copy_record.create_new_list()


    def action_set_cancel(self):
        for record in self:
            if record.state == 'finished':
                raise exceptions.UserError(_('You can not cancel a list that is finished'))
            record.state = 'cancel'

    def create_new_list(self):
        newname = 'Copy of ' + self.name
        new_record = self.name_create(newname)

        self.create_detail_lines(new_record[0], True)
        #return copy.deepcopy(new_record)
        return None

    def create_detail_lines(self, new_id, onlynotinbag):
        if onlynotinbag:
            record_tocheck = self.detail_ids.search([('in_bag', '=', False), ('list_id', '=', self.id)])
        else:
            record_tocheck = self.detail_ids.search([('list_id', '=', self.id)])

        for record in record_tocheck:
            vals = {
                'name': record.name,
                'in_bag': False,
                'remark': record.remark,
                'list_id': new_id,
                'user_created': record.user_created.id,
            }
            record.create(vals)
    def check_products_not_in_bag(self):
        #import ipdb;ipdb.set_trace()
        for record in self.detail_ids:
            if record.search_count([('in_bag', '=', False), ('list_id', '=', record.list_id.id)]) > 0:
                return True
            else:
                return False