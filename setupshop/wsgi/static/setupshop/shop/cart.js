

define(['knockout', 'ko_es5', 'bindings'], function(ko) {
    
    //Cart Item ViewModel
    var CartItemVM = function(cart, data1, data2) {
        var item = {};
        
        // if data2 is set then it's product, variant (user added an item)
        if(data2){
            var product = data1, variant = data2;
            item = {};
            item._subject = "";
            item.rdf_type = new rdf_util.URI("http://setupshop.me/ns#CartItem");
            item.sus_productUrl = new rdf_util.URI(product._subject);
            item.sus_variant = new rdf_util.URI(variant._subject);
            item.sus_unitprice = variant.sus_price;
            item.name = product.dc_title + ' - ' + variant.dc_title;
            item.sus_quantity = 0;            
        }
        // otherwise it's data from the server
        else {
            item = data1;
        }        
        item.view_quantity = item.sus_quantity;
        
        // make quantity properties observable but still act like properties
        ko.track(item, ['sus_quantity', 'view_quantity']);
        
        // quantity functions
        item.quantityChanged = ko.computed(function(){
            if(item.sus_quantity != item.view_quantity){
                return true;
            } else {
                return false;
            }
        });
        item.quantityUpdate = function(callback) {
            if(item.quantityChanged()){
                item.sus_quantity = item.view_quantity;
                item.save(callback);
            }
            else if(callback && typeof callback === 'function')
                callback(item);
        }    
                
        item.lineitem_price = ko.computed(function(){
            return item.sus_quantity * item.sus_unitprice;
        });
        
        item.save = function() {  
            if(item._subject == ""){
                // it's a new item
                var itemPost = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(item);
                ld_util.send_create(cart.cartItemsUrl, itemPost, function(postResponse){
                    cart.loadItems();    
                });
            }
            else {
                //var itemPatch = item.make_patch();
                // it's an existing item and only the quantity has changed
                var itemPatch = {
                        _subject: item._subject,
                        sus_quantity: item.sus_quantity
                }
                itemPatch = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(itemPatch);
                ld_util.send_patch(item._subject, item.ce_revision, itemPatch,function(patchResponse){
                    var responseJso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(patchResponse);
                    //item.request = patchResponse;
                    item.ce_revision = responseJso.ce_revision;                        
                });
            }            
        }
        
        item.deleteItem = function(){
            ld_util.send_delete(item._subject);
        }        
        
        return item;
    }

    //Cart ViewModel
    var CartVM = function() {
        var self = this;

        // cart data
        self.data = {
            _subject: self.cartUrl,
            rdf_type: new rdf_util.URI("http://setupshop.me/ns#Cart"),            
            sus_items: ko.observableArray([])
        }
        self.data = ko.observable(self.data);
        
        // store url, cartUrl, cartItemsUrl
        self.store = null;
        self.cartUrl = null;
        self.cartItemsUrl = null;
        
        // We need to get the store, which knows the cart url
        ld_util.get("/", function(storeResponse){
            self.store = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(storeResponse);
            self.cartUrl = self.store.ce_user.sus_cart.toString();
            // get the cart data using the cartURL in the store 
            ld_util.get(self.cartUrl, function(cartResponse){
                var cart = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(cartResponse);
                self.cartItemsUrl = cart.sus_cartItems;
                // get the cart items
                self.loadItems();
            });
        })
        
        // get/refresh all the cart items for this cart
        self.loadItems = function(){
            ld_util.get(self.cartItemsUrl, function(cartItemsResponse){
                var cartItems = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(cartItemsResponse);
                cartItems = cartItems.ldp_contains || [];
                for ( var i in cartItems) {
                    cartItems[i] = new CartItemVM(self, cartItems[i]);
                }
                self.data().sus_items(cartItems);
            });  
        }
        
        // computed functions
        self.lineitems = ko.computed(function(){
            return self.data().sus_items();
        });
        self.total = ko.computed(function(){
            var tot = 0;
            var items = self.lineitems();
            for(i=0;i<items.length;i++) {
                tot += items[i].lineitem_price();
            }
            return tot;
        });
        self.changed = ko.computed(function(){
            var items = self.lineitems();
            for(i = 0; i<items.length;i++) {
                var item =items[i]; 
                if(item.quantityChanged())
                    return true;
            } 
            return false;
        });

        self.addToCart = function(product, variant) {
            var item = null;
            var items = self.lineitems();
            // look to see if this product-variant is already in the cart
            for(i=0;i<items.length;i++) {
                if(items[i].sus_variant == variant._subject) {
                    item = items[i];
                    break;
                }
            }
            // If this item variant isn't already in the cart add it
            if(!item) {
                item = new CartItemVM(self, product, variant);                
                self.data().sus_items.push(item);
            }            
            
            // Increment the quantity by 1
            item.view_quantity = Number(item.view_quantity) + 1;
            item.quantityUpdate();
        }

        self.deleteLineitem = function(item){
            item.deleteItem();
            self.data().sus_items.remove(item);            
        }
        
        // visibility stuff for Sammy/ko.postbox
        self.visible = ko.observable(false);
        self.showView = function() {
            self.visible(true);
        };
        self.hideView = function() {
            self.visible(false);
        };
        ko.postbox.subscribe("active_view", function(message) {
            if (message.view == 'cart') {
                self.showView();
                document.title = 'Cart';
            }
            else {
                self.hideView();
                // revert any unsaved quantity changes 
                var items = self.data().sus_items();
                for(i=0;i<items.length;i++){
                    items[i].view_quantity = items[i].sus_quantity;                    
                }
                self.data().sus_items(items);
            }
        }, true);
        
        return self;
    }

    return new CartVM();
    
})

