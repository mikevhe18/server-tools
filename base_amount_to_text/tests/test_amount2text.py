# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestAmount2Text(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(TestAmount2Text, self).setUp(*args, **kwargs)
        self.obj_res_currency = self.env['res.currency']
        self.IDR = self.env.ref('base.IDR')

        return result

    def test_onchange_picking_type_id_1(self):
        currency = self.obj_res_currency.search(
            [('id', '=', self.IDR.id)]
        )
        value_1 = 1000000
        value_2 = 2500350.58
        result_1 = currency.amount_to_text(value_1) + 'Rupiah'
        self.assertEqual(result_1, 'Satu Juta Rupiah')

        rupiah, sen = str(value_2).split(".")
        rupiah = currency.amount_to_text(rupiah)
        sen = currency.amount_to_text(sen)

        result_2 = rupiah + 'Rupiah' + ' Koma ' + sen + 'Sen'
        self.assertEqual(result_2, 'Dua Juta Lima Ratus Ribu Tiga Ratus '
            'Lima Puluh Rupiah Koma Lima Puluh Delapan Sen')
