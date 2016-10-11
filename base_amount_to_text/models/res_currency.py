# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
from openerp.exceptions import except_orm
from openerp.tools.safe_eval import safe_eval as eval

class res_currency(models.Model):
    _inherit = 'res.currency'

    python_amount2text = fields.Text(string='Amount To Text')

    @api.multi
    def amount_to_text(self, currency):
        val = {}

        if self.python_amount2text:
            localdict = {'currency':currency}
            eval(self.python_amount2text, localdict, mode='exec', nocopy=True)
            val = localdict['result']

        return val

    @api.multi
    def amount_to_text_v2(self, currency):
        val = {}
        result=''

        if self.python_amount2text:
            try:
                exec self.python_amount2text in val
                result = val['funct_amount_to_text'](currency)
            except:
                raise except_orm(_('Error!'), _('Wrong python code defined.'))

        return result

    @api.multi
    def button_compute_python(self):
        x =  self.amount_to_text(1000000)
        raise except_orm(_('Compute Python'),
            _("Result: '%s'!") % (x,))
