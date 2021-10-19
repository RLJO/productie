# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details

from odoo import models


class Invoice(models.Model):
    _inherit = "account.move"

    def action_confirm_payment_transaction(self):
        for invoice in self:
            for transaction in invoice.transaction_ids.filtered(
                lambda t: t.state in ["pending", "authorized"] and t.acquirer_id.provider == "on_delivery"
            ):
                transaction._set_transaction_done()
                tx_to_process = transaction.filtered(lambda x: x.state == "done" and x.is_processed is False)
                tx_to_process._post_process_after_done()
