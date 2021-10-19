# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    acquirer_id = fields.Many2one("payment.acquirer")

    def action_confirm_payment_transaction(self):
        for sale in self:
            for transaction in sale.transaction_ids.filtered(
                lambda t: t.state in ["pending", "authorized"] and t.acquirer_id.provider == "on_delivery"
            ):
                transaction._set_transaction_done()
                tx_to_process = transaction.filtered(lambda x: x.state == "done" and x.is_processed is False)
                tx_to_process._post_process_after_done()
