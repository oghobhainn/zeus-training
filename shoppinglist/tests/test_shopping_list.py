from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install','-at_install','Marjan')
class ShoppingListTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(ShoppingListTestCase, cls).setUpClass()

        cls.user_created = cls.env['res.partner'].create({
            'name': 'user create',
        })
        cls.shoppinglist = cls.env['shopping.list'].create({
            'name': 'list to test',
        })
        cls.shoppinglistdetail = cls.env['shopping.list.detail'].create({
            'name': 'product on list',
            'list_id': cls.shoppinglist[0].id,
            'user_created': cls.user_created.id,
        })
        cls.shoppinglistdetail = cls.env['shopping.list.detail'].create({
            'name': 'product 2 on list',
            'list_id': cls.shoppinglist[0].id,
            'user_created': cls.user_created.id,
        })

    def test_action_list(self):
        self.shoppinglistdetail.action_in_bag()
        self.assertRecordValues(self.shoppinglist, [
            {'state': 'in_progress'},
        ])

        if self.env['shopping.list'].search([('state', '=', 'new')]) != 0:
            self.assertRaises(UserError)

        self.shoppinglist.action_set_finished()
        self.assertRecordValues(self.shoppinglist, [
            {'state': 'finished'},
        ])

        if self.env['shopping.list'].search([('state', '=', 'new')]) == 0:
            self.assertRaises(UserError)