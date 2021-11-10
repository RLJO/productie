# ©  2015-2021 Deltatech
# See README.rst file on addons root folder for license details

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def payment_action_capture(self):
        if len(self) == 1:
            if len(self.authorized_transaction_ids) == 1:
                transaction = self.authorized_transaction_ids
                invoiced = sum(self.invoice_ids.filtered(lambda x: x.state != "cancel").mapped("amount_total"))
                amount = self.amount_total - invoiced
                if amount != transaction.amount:  # si daca nu e o diferenta mai mare de 15%
                    transaction.write({"amount": amount})
        super(SaleOrder, self).payment_action_capture()
