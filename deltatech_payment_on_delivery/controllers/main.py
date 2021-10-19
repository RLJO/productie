# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details

import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class OnPaymentController(http.Controller):
    _process_url = "/payment/on_delivery/process/"

    @http.route("/payment/on_delivery/process", type="http", auth="public", csrf=False)
    def on_payment_process(self, **post):
        request.env["payment.transaction"].sudo().form_feedback(post, "on_delivery")
        return werkzeug.utils.redirect("/payment/process")
