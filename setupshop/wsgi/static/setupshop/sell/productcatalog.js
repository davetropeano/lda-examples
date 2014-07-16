"use strict";

;(function() {
    function Product(p) {
        this.dc_title = ko.observable(p.dc_title);
        this.dc_description = ko.observable(p.dc_description);
        this.sus_vendor = ko.observable(p.sus_vendor);
        this.sus_category = ko.observableArray(p.sus_category);
    }

    function ProductsApp() {
        ViewModel.call(this, 'productsapp');

        var self = this;
        self.store = APPLICATION_ENVIRON.initial_simple_jso.sus_store //TEMP ... talk to Dave
        self.products = ko.observableArray();
        self.currentProduct = ko.observable();

        self.inventoryText = function(variants) {
            var qty = 0;
            variants.forEach(function(element) {
                qty += element.sus_inventory_qty;
            });
            return qty + ' in stock for ' + variants.length + ' variants';
        }

        self.editProduct = function(p) {
            self.currentProduct = new Product(p);
            self.showView('editproduct');
        }

        self.importProducts = function() {
            self.showView('importproducts');
            // document.getElementById('import-products-dialog').style.display = 'block'
            // document.getElementById('page-productslist').style.display = 'none'
        }

        self.cancelImport = function() {
            // document.getElementById('import-products-dialog').style.display = 'none'
            // document.getElementById('page-productslist').style.display = 'Block'
        }

        // get the list of products
        // given the store object we have to iterate through the categories
        // to build up the list of products

        ld_util.get(self.store.sus_categories, function(request){
            if (request.status==200) {
                var categories = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request).ldp_contains;
                if (categories)
                    categories.forEach(function(element) {
                        ld_util.get(element.sus_categoryProducts, function(request) {
                            if (request.status == 200) {
                                var products = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request).ldp_contains;
                                if (products)
                                    products.forEach(function(element) {
                                        self.products.push(element);
                                    });
                            }
                            else {
                                console.log(request.status);
                            }
                        });
                    });
            }
            else {
                console.log( request.status )
            }
        });
    };

    inheritPrototype(ProductsApp, ViewModel);

    var productcatalog = new ProductsApp();
    productcatalog.addView('productslist');
    productcatalog.addView('editproduct');
    productcatalog.defaultView = 'productslist';

    window.App = window.App || {};
    App.productcatalog = productcatalog;
}());



