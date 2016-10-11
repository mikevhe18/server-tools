# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
from openerp.tools.safe_eval import safe_eval as eval

PYTHON_IDR = """result=''
if currency > 0:
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

    ns = str(currency)

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


class res_currency(models.Model):
    _inherit = 'res.currency'

    python_amount2text = fields.Text(
        string='Amount To Text')

    @api.multi
    def amount_to_text(self, value):
        val = {}
        self.ensure_one()
        if self.python_amount2text:
            localdict = {'currency': value}
            eval(self.python_amount2text, localdict, mode='exec', nocopy=True)
            val = localdict['result']

        return val

    @api.model
    def _install_python_IDR(self):
        records = self.search([('name', '=', 'IDR')])
        if records:
            records.python_amount2text = PYTHON_IDR
