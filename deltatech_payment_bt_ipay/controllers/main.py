# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details

import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class BTiPayController(http.Controller):
    _confirm_url = "/payment/bt_ipay/payment/"
    _return_url = "/payment/bt_ipay/return/"

    @http.route("/payment/bt_ipay/payment", type="http", auth="none", methods=["POST"], csrf=False)
    def ipay_payment(self, **post):

        return werkzeug.utils.redirect(post["formUrl"])

    @http.route("/payment/bt_ipay/return/<int:acquirer_id>", type="http", auth="public", csrf=False)
    def ipay_return(self, acquirer_id, **post):
        """iPay return
        return – a URL in your web application where the client will be redirected to once
        the payment is complete. Not to be confused with a success or cancel URL, the
        information displayed here is dynamic, based on the information previously sent to
        confirm URL.
        """
        _logger.info("Beginning iPay return form_feedback with post data %s", str(post))  # debug

        if post:
            post["acquirer_id"] = acquirer_id
            request.env["payment.transaction"].sudo().form_feedback(post, "bt_ipay")

        return werkzeug.utils.redirect("/payment/process")
