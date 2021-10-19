odoo.define("deltatech_payment_on_delivery.TransactionValidationView", function (require) {
    "use strict";

    var TransactionValidationController = require("deltatech_payment_on_delivery.TransactionValidationController");
    var ListView = require("web.ListView");
    var viewRegistry = require("web.view_registry");

    var TransactionValidationView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TransactionValidationController,
        }),
    });

    viewRegistry.add("transaction_validate_button", TransactionValidationView);
});
