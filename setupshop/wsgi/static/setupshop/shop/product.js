define(['cart', 'toastr', 'knockout', 'ko_es5'], function(cartVM, toastr, ko) {
    var ProductVM = function() {
        var self=this;
        self.product = null;
        self.visible = false;

        self.showView = function(product) {
            // augment each option with a selectedOption attribute
            ko.utils.arrayForEach(product.sus_options, function(option) {
                option.selectedOption = option.sus_option_values[0];
                ko.track(option);
            });

            self.product = product;
            document.title = product.dc_title;
            self.visible = true;
        };

        self.addToCart = function() {
            cartVM.addToCart(self.product, self.selectedVariant);

            toastr.options.timeOut = 1500;
            // toastr.options.positionClass = 'toast-top-full-width';
            toastr.success(self.product.dc_title, 'Added to cart');
        };

        self.hideView = function() {
            self.visible = false;
        };

        ko.track(this);

        ko.defineProperty(this, 'selectedVariant', function() {
            var path = ko.utils.arrayMap(self.product.sus_options, function(option) {
                return option.selectedOption;
            });

            path = path.join('/');
            var v = ko.utils.arrayFirst(self.product.sus_variants, function(variant) {
                return path == variant.dc_title;
            });

            return v;
        });

        ko.postbox.subscribe("active_view", function(message) {
            if (message.view == 'product')
                self.showView(message.data);
            else
                self.hideView();
        }, true);

    };

    return new ProductVM();
});