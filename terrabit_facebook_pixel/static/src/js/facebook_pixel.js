odoo.define("terrabit_faccebook_pixel.events", function (require) {
    "use strict";

    // Website_sale.tracking

    var publicWidget = require("web.public.widget");

    publicWidget.registry.websiteSaleFacebookEvents = publicWidget.Widget.extend({
        selector: ".oe_website_sale",
        events: {
            'click form[action="/shop/cart/update"] a.a-submit': "async _onAddProductIntoCart",
            'click a[href="/shop/checkout"]': "_onCheckoutStart",
            'click div.oe_cart a[href^="/web?redirect"][href$="/shop/checkout"]': "async _onCustomerSignin",

            'click a[href="/shop/checkout?express=1"]': "async _onCheckoutStart",
            "click .o_add_wishlist, .o_add_wishlist_dyn": "async _onAddToWishlist",

            "submit .o_wsale_products_searchbar_form": "async _onSearch",
        },

        start: function () {
            // Watching a product
            if (this.$el.is("#product_detail")) {
                var content_name = this.$('[itemprop="name"]').text();
                var price = this.$('[itemprop="price"]').text();
                var priceCurrency = this.$('[itemprop="priceCurrency"]').text();
                var content_category = this.$('[itemprop="category"]').text();
                var productID = this.$('input[name="product_id"]').attr("value");
                this._track_facebook("track", "ViewContent", {
                    content_name: content_name,
                    content_category: content_category,
                    content_type: "product",
                    content_ids: [productID],
                    value: price,
                    currency: priceCurrency,
                });
            }
        },

        _track_facebook: function () {
            var websiteFBQ =
                window.fbq ||
                function () {
                    // Do nothing.
                };
            websiteFBQ.apply(this, arguments);
        },

        _onAddProductIntoCart: function (ev) {
            var $el = $(ev.currentTarget);

            var $form = $el.closest("form");
            var templateId = $form.find(".product_template_id").val();
            // When adding from /shop instead of the product page, need another selector
            if (!templateId) {
                templateId = $el.data("product-template-id");
            }
            this._track_facebook("track", "AddToCart", {content_type: "product", content_ids: [templateId]});
        },

        _onCheckoutStart: function () {
            this._track_facebook("track", "InitiateCheckout");
        },

        _onOrderPayment: function () {
            this._track_facebook("track", "AddPaymentInfo");
        },

        _onSearch: function () {
            this._track_facebook("track", "Search");
        },

        _onAddToWishlist: function (ev) {
            var $el = $(ev.currentTarget);

            var $form = $el.closest("form");
            var templateId = $form.find(".product_template_id").val();
            // When adding from /shop instead of the product page, need another selector
            if (!templateId) {
                templateId = $el.data("product-template-id");
            }

            this._track_facebook("track", "AddToWishlist", {content_type: "product", content_ids: [templateId]});
        },

        _onCustomerSignin: function () {
            this._track_facebook("track", "Subscribe");
        },
    });

    /*
    PublicWidget.registry.PaymentFormFacebookEvents = publicWidget.Widget.extend({
        selector: ".o_payment_form",
        events: {
            "click #o_payment_form_pay": "_onOrder",
        },

        _track_facebook: function() {
            var websiteFBQ = window.fbq || function() {
            // do nothing.
            };
            websiteFBQ.apply(this, arguments);
        },
        _onOrder: function() {
            this._track_facebook("track", "Purchase");
        },
    });
*/

    publicWidget.registry.ConfirmationFormFacebookEvents = publicWidget.Widget.extend({
        selector: ".oe_website_sale_confirmation",

        start: function () {
            var amount_total = this.$el.data("amount_total");
            var currency = this.$el.data("currency");
            var values = {
                currency: currency,
                value: amount_total,
            };
            this._track_facebook("track", "Purchase", values);
        },

        _track_facebook: function () {
            var websiteFBQ =
                window.fbq ||
                function () {
                    // Do nothing.
                };
            websiteFBQ.apply(this, arguments);
        },
    });
});
