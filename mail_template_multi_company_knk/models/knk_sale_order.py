# -*- coding: utf-8 -*-
###############################################################################
# Author : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
###############################################################################
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _find_mail_template(self, force_confirmation_template=False):
        res = super(SaleOrder, self)._find_mail_template(force_confirmation_template=False)
        template = self.env['mail.template'].search([('model_id.model', '=', self._name), ('company_id', '=', self.company_id.id)], limit=1)
        if template:
            return template.id
        return res

