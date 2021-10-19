# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details


import logging
import pprint

from odoo import _, api, fields, models

from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class OnDeliveryAcquirer(models.Model):
    _inherit = "payment.acquirer"

    submit_txt = fields.Char(string="Submit text", default="Pay", translate=True)
    provider = fields.Selection(selection_add=[("on_delivery", "On Delivery")], ondelete={"on_delivery": "set default"})

    def _get_feature_support(self):
        res = super(OnDeliveryAcquirer, self)._get_feature_support()
        res["authorize"].append("on_delivery")
        return res

    def on_delivery_get_form_action_url(self):
        # base_url = self.get_base_url()
        return "/payment/on_delivery/process"

    def on_delivery_form_generate_values(self, values):
        # values['return_url'] = '/payment/on_payment/process'
        values["tx_url"] = "/payment/on_delivery/process"

        return values


class OnDeliveryTransaction(models.Model):
    _inherit = "payment.transaction"

    def on_delivery_s2s_void_transaction(self):
        self._set_transaction_cancel()

    def on_delivery_s2s_capture_transaction(self):
        self._set_transaction_done()
        tx_to_process = self.filtered(lambda x: x.state == "done" and x.is_processed is False)
        tx_to_process._post_process_after_done()

    def _prepare_account_payment_vals(self):
        values = super(OnDeliveryTransaction, self)._prepare_account_payment_vals()
        if self.env.context.get("payment_date"):
            values["payment_date"] = self.env.context["payment_date"]
        return values

    def _on_delivery_form_validate(self, data):
        # _logger.info('Validated on delivery payment for tx %s: set as pending' % (self.reference))
        # self._set_transaction_pending()
        _logger.info("Validated on delivery payment for tx %s: set as authorized" % self.reference)
        self._set_transaction_authorized()
        return True

    @api.model
    def _on_delivery_form_get_tx_from_data(self, data):
        reference = data.get("reference")
        tx = self.search([("reference", "=", reference)])

        if not tx or len(tx) > 1:
            error_msg = _("received data for reference %s") % (pprint.pformat(reference))
            if not tx:
                error_msg += _("; no order found")
            else:
                error_msg += _("; multiple order found")
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        return tx
