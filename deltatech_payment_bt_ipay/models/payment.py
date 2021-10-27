# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details

import json
import logging
import unicodedata

import requests

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.phone_validation.tools import phone_validation

_logger = logging.getLogger(__name__)


class BTiPayAcquirer(models.Model):
    _inherit = "payment.acquirer"

    provider = fields.Selection(selection_add=[("bt_ipay", "BT iPay")], ondelete={"bt_ipay": "set default"})
    bt_ipay_user = fields.Char()
    bt_ipay_pass = fields.Char()
    bt_mode = fields.Selection([("1", "1 Phase"), ("2", "2 Phase")])

    @api.onchange("bt_mode")
    def onchange_bt_mode(self):
        if self.bt_mode == "2":
            self.capture_manually = True
        else:
            self.capture_manually = False

    def _get_feature_support(self):
        res = super(BTiPayAcquirer, self)._get_feature_support()
        res["authorize"].append("bt_ipay")
        return res

    def bt_ipay_get_form_action_url(self):
        environment = "prod" if self.state == "enabled" else "test"
        if environment == "prod":
            url = "https://ecclients.btrl.ro/payment"
        else:
            url = "https://ecclients.btrl.ro:5443/payment"
        return url

    def bt_ipay_form_generate_values(self, values):
        def strip_accents(text):
            text = unicodedata.normalize("NFD", text or "").encode("ascii", "ignore").decode("utf-8")
            return str(text)

        base_url = self.get_base_url()

        bt_currency_code = {"RON": "946", "EUR": "978", "USD": "840"}

        currency = bt_currency_code.get(values["currency"].name)

        if values.get("partner_phone"):
            try:
                phone = values.get("partner_phone")
                country = self.env["res.country"].sudo().browse(values.get("partner_country_id"))
                phone = phone_validation.phone_format(
                    phone,
                    country.code if country else None,
                    country.phone_code if country else None,
                    force_format="E164",
                    raise_exception=True,
                )
                values["partner_phone"] = phone.replace("+", "")
            except Exception as e:
                _logger.error(e.name)
                raise ValidationError(e.name)

        customerDetails = {
            "email": values["partner_email"],
            "phone": values["partner_phone"],
            "deliveryInfo": {
                "deliveryType": "comanda",
                "country": "642",
                "city": strip_accents(values["partner_city"]),
                "postAddress": strip_accents(values["partner_address"]),
                "postalCode": values["partner_zip"],
            },
            "billingInfo": {
                "country": "642",
                "city": strip_accents(values["billing_partner_city"]),
                "postAddress": strip_accents(values["billing_partner_address"]),
                "postAddress2": strip_accents(values["billing_partner_address"]),
                "postAddress3": strip_accents(values["billing_partner_address"]),
                "postalCode": values["billing_partner_zip"],
            },
        }

        orderBundle = {"orderCreationDate": fields.Date.to_string(self.create_date), "customerDetails": customerDetails}

        bt_ipay_tx_values = {
            "userName": self.bt_ipay_user,
            "password": self.bt_ipay_pass,
            "orderNumber": values["reference"],
            "amount": int(values["amount"] * 100),
            "currency": currency,
            "returnUrl": (base_url + "payment/bt_ipay/return/" + str(self.id)),
            "description": "Plata online cu cardul",
            "jsonParams": '{"FORCE_3DS2":"true"}',
            "orderBundle": json.dumps(orderBundle),
        }

        if not self.capture_manually:
            # 1 Phase
            url = self.bt_ipay_get_form_action_url() + "/rest/register.do"
        else:
            # 2 Phase
            url = self.bt_ipay_get_form_action_url() + "/rest/registerPreAuth.do"

        req = requests.post(url, bt_ipay_tx_values)
        response_text = req.content
        req.raise_for_status()
        data = json.loads(response_text)
        _logger.info(data)
        if data.get("errorMessage"):
            _logger.error(data)
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
        if data["errorCode"] != "0":
            _logger.error(data["errorMessage"])
            # tx.write({"state_message": data["errorMessage"]})
            tx._set_transaction_error(data["errorMessage"])

            return False
        if data["actionCode"] != 0:
            _logger.error(data["actionCodeDescription"])
            # tx.write({"state_message": data["actionCodeDescription"]})

            actionCodeDescription = {
                320: _("Card inactiv. Vă rugăm activați cardul."),
                801: _("Emitent indisponibil."),
                803: _("Card blocat. Vă rugăm contactați banca emitentă."),
                805: _("Tranzacție respinsă."),
                861: _("Dată expirare card greșită."),
                871: _("CVV gresit."),
                905: _("Card invalid. Acesta nu există în baza de date."),
                906: _("Card expirat."),
                914: _("Cont invalid. Vă rugăm contactați banca emitentă."),
                915: _("Fonduri insuficiente."),
                917: _("Limită tranzacționare depășită."),
                998: _(
                    "Tranzacția în rate nu este permisă cu acest card."
                    " Te rugăm să folosești un card de credit emis de Banca Transilvania."
                ),
                341016: _("3DS2 authentication is declined by Authentication Response (ARes) – issuer"),
                341017: _("3DS2 authentication status in ARes is unknown - issuer"),
                341018: _("3DS2 CReq cancelled - client"),
                341019: _("3DS2 CReq failed - client/issuer"),
                341020: _("3DS2 unknown status in RReq - issuer"),
            }
            msg = actionCodeDescription.get(data["actionCode"], data["actionCodeDescription"])
            tx._set_transaction_error(msg)

            return False

        if self.acquirer_id.bt_mode == "1" and data["orderStatus"] == 2:
            tx._set_transaction_done()
        if self.acquirer_id.bt_mode == "2" and data["orderStatus"] == 1:
            tx._set_transaction_authorized()

        return True

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
            _logger.info("Pentru referinta {} a fost identificata tranzatia {} ".format(reference, tx.reference))

        return tx

    def bt_ipay_s2s_void_transaction(self):
        url = self.acquirer_id.bt_ipay_get_form_action_url() + "/rest/reverse.do"
        params = {
            "userName": self.acquirer_id.bt_ipay_user,
            "password": self.acquirer_id.bt_ipay_pass,
            "orderId": self.acquirer_reference,
        }
        req = requests.post(url, params)
        response_text = req.content
        req.raise_for_status()
        data = json.loads(response_text)
        if data["errorCode"] == "0":
            self._set_transaction_cancel()
        else:
            raise ValidationError(data["errorMessage"])

    def bt_ipay_s2s_capture_transaction(self):
        url = self.acquirer_id.bt_ipay_get_form_action_url() + "/rest/deposit.do"

        params = {
            "userName": self.acquirer_id.bt_ipay_user,
            "password": self.acquirer_id.bt_ipay_pass,
            "orderId": self.acquirer_reference,
            "amount": int(self.amount * 100),
        }
        req = requests.post(url, params)
        response_text = req.content
        req.raise_for_status()
        data = json.loads(response_text)
        if data["errorCode"] == "0":
            self._set_transaction_done()
            self._post_process_after_done()
        else:
            raise ValidationError(data["errorMessage"])
