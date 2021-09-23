# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details


from . import controllers
from . import models
from . import wizard

from odoo.addons.payment.models.payment_acquirer import create_missing_journal_for_acquirers
from odoo.addons.payment import reset_payment_provider


def uninstall_hook(cr, registry):
    reset_payment_provider(cr, registry, "on_delivery")
