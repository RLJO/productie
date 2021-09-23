odoo.define("deltatech_payment_on_delivery.TransactionValidationController", function (require) {
    "use strict";

    var core = require("web.core");
    var ListController = require("web.ListController");

    var _t = core._t;
    var qweb = core.qweb;

    var TransactionValidationController = ListController.extend({
        events: _.extend(
            {
                "click .o_button_validate_transaction": "_onValidateTransaction",
                "click .o_button_import_transaction": "_onImportTransaction",
                "click .o_button_clear_transaction": "_onClearTransaction",
            },
            ListController.prototype.events
        ),
        /**
         * @override
         */
        init: function (parent, model, renderer) {
            var context = renderer.state.getContext();
            this.transaction_id = context.active_id;
            this.transaction_ids = context.active_ids;
            return this._super.apply(this, arguments);
        },

        // -------------------------------------------------------------------------
        // Public
        // -------------------------------------------------------------------------

        /**
         * @override
         */
        // renderButtons: function ($node) {
        //     this._super.apply(this, arguments);
        //     var $validationButton = $(qweb.render("TransactionLines.Buttons"));
        //     $validationButton.prependTo($node.find(".o_list_buttons"));
        // },

        renderButtons: function () {
            this._super.apply(this, arguments);
            this.$buttons.find(".o_button_import").addClass("d-none");
            var $validationButton = $(qweb.render("TransactionLines.Buttons"));
            this.$buttons.prepend($validationButton);
        },

        // -------------------------------------------------------------------------
        // Handlers
        // -------------------------------------------------------------------------

        _onImportTransaction: function () {
            this.do_action({
                name: "Import transactions",
                res_model: "payment.transaction.import.file",
                views: [[false, "form"]],
                type: "ir.actions.act_window",
                view_mode: "form",
                target: "new",
            });
        },

        _onClearTransaction: function () {
            var self = this;
            var prom = Promise.resolve();
            var recordID = this.renderer.getEditableRecordID();
            if (recordID) {
                // If user's editing a record, we wait to save it before to try to
                // validate the .
                prom = this.saveRecord(recordID);
            }

            self.transaction_ids = this.getSelectedIds();

            prom.then(function () {
                self._rpc({
                    model: "payment.transaction.import",
                    method: "unlink",
                    args: [self.transaction_ids],
                }).then(function () {
                    self.trigger_up("reload");
                });
            });
        },

        _onValidateTransaction: function () {
            var self = this;
            var prom = Promise.resolve();
            var recordID = this.renderer.getEditableRecordID();
            if (recordID) {
                // If user's editing a record, we wait to save it before to try to
                // validate the .
                prom = this.saveRecord(recordID);
            }
            self.transaction_ids = this.getSelectedIds();

            prom.then(function () {
                self._rpc({
                    model: "payment.transaction.import",
                    method: "action_validate",
                    args: [self.transaction_ids],
                }).then(function (res) {
                    var exitCallback = function (infos) {
                        // In case we discarded a wizard, we do nothing to stay on
                        // the same view...

                        if (infos && infos.special) {
                            return;
                        }

                        // ... but in any other cases, we go back on the transaction form.
                        self.do_notify(_t("Success"), _t("The transaction has been processed"));
                        self.trigger_up("history_back");
                    };

                    if (_.isObject(res)) {
                        self.do_action(res, {on_close: exitCallback});
                    } else {
                        return exitCallback();
                    }
                    self.trigger_up("reload");
                });
            });
        },
    });

    return TransactionValidationController;
});
