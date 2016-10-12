# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
from openerp.tools.safe_eval import safe_eval as eval


class ResLang(models.Model):
    _inherit = 'res.lang'

    python_amount2text = fields.Text(
        string='Amount To Text')

    @api.multi
    def amount_to_text(self, value):
        val = {}
        self.ensure_one()
        if self.python_amount2text:
            localdict = {'value': value}
            eval(self.python_amount2text, localdict, mode='exec', nocopy=True)
            val = localdict['result']

        return val
