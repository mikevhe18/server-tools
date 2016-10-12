# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase

PYTHON_IDR = """result=''
if value > 0:
    ones = [
        "", "Satu ","Dua ","Tiga ","Empat ", "Lima ","Enam ",
        "Tujuh ","Delapan ","Sembilan "
    ]
    tens = [
        "Sepuluh ","Sebelas ","Dua Belas ","Tiga Belas ",
        "Empat Belas ","Lima Belas ","Enam Belas ",
        "Tujuh Belas ","Delapan Belas ","Sembilan Belas "
    ]
    twenties = [
        "","","Dua Puluh ","Tiga Puluh ","Empat Puluh ",
        "Lima Puluh ","Enam Puluh ","Tujuh Puluh ",
        "Delapan Puluh ","Sembilan Puluh "
    ]
    thousands = ["","Ribu ","Juta ", "Milyar "]

    n3 = []
    r1 = ""

    ns = str(value)

    for k in range(3, 33, 3):
        r = ns[-k:]
        q = len(ns) - k
        if q < -2:
            break
        else:
            if q >= 0:
                n3.append(int(r[:3]))
            elif q >= -1:
                n3.append(int(r[:2]))
            elif q >= -2:
                n3.append(int(r[:1]))
        r1 = r

    for i, x in enumerate(n3):
        b1 = x % 10
        b2 = (x % 100)//10
        b3 = (x % 1000)//100
        if x == 0:
            continue
        else:
            t = thousands[i]
        if b2 == 0:
            if b1 == 1:
                result = 'se' + t + result
            else:
                result = ones[b1] + t + result
        elif b2 == 1:
            result = tens[b1] + t + result
        elif b2 > 1:
            result = twenties[b2] + ones[b1] + t + result
        if b3 > 0:
            result = ones[b3] + "Ratus " + result

    result = result.replace("seJuta", "Satu Juta")
    result = result.replace("seMilyar", "Satu Milyar")
    result = result.replace("Satu Ratus", "Seratus")
"""


class TestAmount2Text(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(TestAmount2Text, self).setUp(*args, **kwargs)
        self.obj_res_lang = self.env['res.lang']

        return result

    def _prepare_languange_IDR(self):
        data = {
            'code': 'id_IDR',
            'name': 'Indonesia',
            'translatable': 'translatable',
            'python_amount2text': PYTHON_IDR,
        }
        return data

    def test_amount_to_text(self):
        # Create Languanges
        data_languange = self._prepare_languange_IDR()
        lang = self.obj_res_lang.\
            create(data_languange)

        # Check Create Languanges
        self.assertIsNotNone(lang)

        # Variables
        value_1 = 1000000
        value_2 = 2500350.58

        # Check Method Amount To Text Using Variable 1
        result_1 = lang.amount_to_text(value_1) + 'Rupiah'
        self.assertEqual(result_1, 'Satu Juta Rupiah')

        # Check Method Amount To Text Using Variable 2
        rupiah, sen = str(value_2).split(".")
        rupiah = lang.amount_to_text(rupiah)
        sen = lang.amount_to_text(sen)

        result_2 = rupiah + 'Rupiah' + ' Koma ' + sen + 'Sen'
        self.assertEqual(
            result_2,
            'Dua Juta Lima Ratus Ribu Tiga Ratus '
            'Lima Puluh Rupiah Koma Lima Puluh Delapan Sen')
