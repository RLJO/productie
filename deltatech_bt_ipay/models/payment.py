# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details

import json
import logging

import requests

from odoo import api, fields, models

from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class BTiPayAcquirer(models.Model):
    _inherit = "payment.acquirer"

    provider = fields.Selection(selection_add=[("bt_ipay", "BT iPay")], ondelete={"bt_ipay": "set default"})
    bt_ipay_user = fields.Char()
    bt_ipay_pass = fields.Char()
    bt_mode = fields.Selection([("1", "1 Phase"), ("2", "2 Phase")])

    def bt_ipay_get_form_action_url(self):
        environment = "prod" if self.state == "enabled" else "test"
        if environment == "prod":
            url = "https://ecclients.btrl.ro/payment"
        else:
            url = "https://ecclients.btrl.ro:5443/payment"
        return url

    def bt_ipay_form_generate_values(self, values):
        base_url = self.get_base_url()

        if values["currency"].name == "RON":
            currency = "946"
        else:
            currency = ""  # de implementat codul si pentru alte valute

        bt_ipay_tx_values = {
            "userName": self.bt_ipay_user,
            "password": self.bt_ipay_pass,
            "orderNumber": values["reference"],
            "amount": int(values["amount"] * 100),
            "currency": currency,
            "returnUrl": (base_url + "payment/bt_ipay/return/" + str(self.id)),
            "description": "Plata online cu cardul",
        }

        url = self.bt_ipay_get_form_action_url() + "/rest/register.do"
        req = requests.post(url, bt_ipay_tx_values)
        response_text = req.content
        req.raise_for_status()
        data = json.loads(response_text)
        _logger.info(data)
        if data.get("errorMessage"):
            raise ValidationError(data["errorMessage"])

        bt_ipay_tx_values.update(data)

        bt_ipay_tx_values["mdOrder"] = data["orderId"]
        bt_ipay_tx_values["payment_url"] = "/payment/bt_ipay/payment/"
        bt_ipay_tx_values["acquirer_reference"] = data["orderId"]
        tx = self.env["payment.transaction"].search([("reference", "=", values["reference"])])
        tx.write({"acquirer_reference": data["orderId"]})

        return bt_ipay_tx_values

    def bt_ipay_compute_fees(self, amount, currency_id, country_id):
        """
        computes the fees of the acquirer, using generic fields defined on the acquirer
           model (see fields definition)
        :param amount:
        :param currency_id:
        :param country_id:
        :return:
        """
        return 0.0


class BTiPayTransaction(models.Model):
    _inherit = "payment.transaction"

    def bt_ipay_create(self, values):
        return {}

    def _bt_ipay_form_validate(self, data):
        _logger.info("iPay form validate with post data %s", str(data))
        # acum sa determin care e situatia cu plata

        reference = data["orderId"]
        params = {
            "userName": self.acquirer_id.bt_ipay_user,
            "password": self.acquirer_id.bt_ipay_pass,
            "orderId": data["orderId"],
        }
        url = self.acquirer_id.bt_ipay_get_form_action_url() + "/rest/getOrderStatusExtended.do"
        req = requests.post(url, params)
        response_text = req.content
        req.raise_for_status()
        data = json.loads(response_text)
        _logger.info(data)
        self.write({"state_message": response_text})
        # self.env.cr.commit()

        tx = self.search([("acquirer_reference", "=", reference)])
        _logger.info(tx.id)
        _logger.info(self.id)
        if data["orderStatus"] == 2:
            tx._set_transaction_done()
            return True
        else:
            tx._set_transaction_cancel()
            return False

    @api.model
    def _bt_ipay_form_get_tx_from_data(self, data):
        """Given a data dict coming from ipay, verify it and find the related
        transaction record."""

        origin_data = dict(data)

        acquirer_id = origin_data["acquirer_id"]
        reference = data["orderId"]
        _logger.info("iPay get_tx_from_data with post data %s", str(data))

        self.env["payment.acquirer"].browse(acquirer_id)
        # environment = "prod" if acquirer.state == "enabled" else "test"

        tx = self.search([("acquirer_reference", "=", reference)])
        if tx:
            _logger.info("Pentru referinta  {} a fost identificata tranzatia {} ".format(reference, tx.reference))

        return tx
