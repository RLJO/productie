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
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    company_id = fields.Many2one('res.company', string='Company', help="Here You Select the Company Which Are Send The Mail Template Of That Company.")

    is_read_only = fields.Boolean(string="Copy template")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {},
                       name=_("%s (copy)") % self.name)
        default.update({'is_read_only': True})
        return super(MailTemplate, self).copy(default=default)

    @api.constrains('company_id')
    def validate_company_id(self):
        for record in self:
            if record.company_id:
                templates = self.env['mail.template'].search([('model_id.model', '=', record.model_id.model), ('company_id', '=', record.company_id.id), ('id', '!=', record.id)], limit=1)
                if templates:
                    raise UserError(_("You can not select this %s company. It is already configure in this template %s ") % (record.company_id.name, templates.name))
