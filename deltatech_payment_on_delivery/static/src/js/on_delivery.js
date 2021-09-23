odoo.define("deltatech_payment_on_delivery.payment_on_delivery", function (require) {
    "use strict";

    var core = require("web.core");
    var _t = core._t;

    var PaymentForm = require("payment.payment_form");

    PaymentForm.include({
        updateNewPaymentDisplayStatus: function () {
            var checked_radio = this.$('input[type="radio"]:checked');
            var acquirer_id = $(checked_radio).data("acquirer-id");
            var submit_txt = _t("Finalize order");
            if (acquirer_id) {
                var input_submit_txt = this.$('input[name="acq_submit_txt_' + acquirer_id + '"]');
                submit_txt = $(input_submit_txt).data("submit_txt");
            }
            var $pay_button = $("button#o_payment_form_pay");
            $pay_button.html(submit_txt + ' <i class="fa fa-chevron-right">');
            this._super.apply(this, arguments);
        },
    });
});
