# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details
import base64
import logging

import xlrd

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PaymentTransactionImportFile(models.TransientModel):
    _name = "payment.transaction.import.file"
    _description = "Import file payment transaction"

    carrier_id = fields.Many2one("delivery.carrier", string="Carrier", required=True)
    name = fields.Char(string="File Name")
    data_file = fields.Binary(string="File", required=True)

    def do_import(self):
        decoded_data = base64.b64decode(self.data_file)
        book = xlrd.open_workbook(file_contents=decoded_data)
        sheet = book.sheet_by_index(0)
        table_values = []

        for row in list(map(sheet.row, range(sheet.nrows))):
            values = []
            for cell in row:
                if cell.ctype is xlrd.XL_CELL_NUMBER:
                    is_float = cell.value % 1 != 0.0
                    values.append(str(cell.value) if is_float else str(int(cell.value)))
                else:
                    values.append(cell.value)
            table_values.append(values)

        delivery_type = self.carrier_id.delivery_type
        if hasattr(self, "%s_do_import" % delivery_type):
            getattr(self, "%s_do_import" % delivery_type)(table_values)
        else:
            pass
        action = self.env.ref("deltatech_payment_on_delivery.action_payment_transaction_import").read()[0]

        return action


class PaymentTransactionImport(models.TransientModel):
    _name = "payment.transaction.import"
    _description = "Import payment transaction"

    transaction_id = fields.Many2one("payment.transaction", string="Transaction", readonly=True)
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")

    acquirer_reference = fields.Char(string="Acquirer Reference")
    carrier_tracking_ref = fields.Char(string="Tracking Reference")

    amount = fields.Float(string="Amount")
    date = fields.Date(string="Date")
    date_text = fields.Char(string="Date as Text")
    state = fields.Selection(
        [("draft", "Draft"), ("done", "Done"), ("error", "Error")],
        string="Status",
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    def action_validate(self):

        for item in self:
            if not item.transaction_id and item.acquirer_reference:
                domain = [("reference", "=", item.acquirer_reference)]
                transaction = self.env["payment.transaction"].search(domain, limit=1)
                if transaction:
                    item.write({"transaction_id": transaction.id})
            if not item.transaction_id and item.acquirer_reference:
                domain = [("acquirer_reference", "=", item.acquirer_reference)]
                transaction = self.env["payment.transaction"].search(domain, limit=1)
                if transaction:
                    item.write({"transaction_id": transaction.id})
            if not item.transaction_id and item.carrier_tracking_ref:
                domain = [("acquirer_reference", "=", item.carrier_tracking_ref)]
                transaction = self.env["payment.transaction"].search(domain, limit=1)
                if transaction:
                    item.write({"transaction_id": transaction.id})

            if item.transaction_id and item.amount == item.transaction_id.amount:
                item.write({"state": "done"})
                if item.transaction_id.state != "done":
                    transaction = item.transaction_id.with_context(payment_date=item.date)
                    transaction._set_transaction_done()
                    transaction._reconcile_after_transaction_done()
            else:
                item.write({"state": "error"})

        return True
