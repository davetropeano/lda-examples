//Cart Item ViewModel
    var CartItemVM = function(cart, data1, data2) {
        var item = {};
        //if data2 is set then it's product, variant (user added an item)
        if(data2){
            var product = data1, variant = data2;
            item = {};
            item._subject = "#item" + cart.data().sus_lineitem_nextId.toString();
            item.rdf_type = new rdf_util.URI("http://setupshop.me/ns#ShoppingCartItem");
            item.sus_productUrl = new rdf_util.URI(product._subject);
            item.sus_variant = new rdf_util.URI(variant._subject);
            item.sus_quantity = ko.observable(0);
            item.sus_unitprice = variant.sus_price;
            item.name = product.dc_title + ' - ' + variant.dc_title;
            item.lineitem_price = ko.computed(function(){return item.sus_quantity() * item.sus_unitprice;});

        }
        //Otherwise it's data from the server
        else {
            item = data1;
            item.sus_quantity = ko.observable(item.sus_quantity);
            item.lineitem_price = ko.computed(function(){return item.sus_quantity() * item.sus_unitprice;});
        }
        
        //View Quantity
        item.view_quantity = ko.observable(item.sus_quantity());
        
        //Quantity changed
        item.quantityChanged = ko.computed(function(){
            if(item.sus_quantity() != item.view_quantity()){
                return true;
            } else {
                return false;
            }
        });
        item.quantityUpdate = function() {
            item.sus_quantity(item.view_quantity());
            cart.save();
        }        
        return item;
    }

    //Cart ViewModel
    var CartVM = function() {
        var self = this;

        // visible stuff
        self.visible = ko.observable(false);
        self.showView = function() {
            self.visible(true);
        };
        self.hideView = function() {
            self.visible(false);
        };

        // cart data
        self.data = {
            _subject: self.cartUrl,
            rdf_type: new rdf_util.URI("http://setupshop.me/ns#ShoppingCart"),
            sus_lineitem_nextId: 0,
            sus_items: ko.observableArray([])
        }
        self.data = ko.observable(self.data);

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
            var items = self.data().sus_items();
            for(i = 0; i<items.length;i++) {
                var item =items[i]; 
                if(item.quantityChanged())
                    return true;
            } 
            return false;
        });

        // store url stuff
        self.store = null;
        self.cartUrl = null;
        //Have to get the store, which knows the cart url
        ld_util.get("/", function(response){
            self.store = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(response);
            self.cartUrl = self.store.ce_user.sus_cart.toString();
            //load cart from server
            ld_util.get(self.cartUrl, self.loadResponseData);
        })

        self.addToCart = function(product, variant) {
            var item = null;
            var items = self.lineitems();
            //look to see if this is already in the cart
            for(i=0;i<items.length;i++) {
                if(items[i].sus_variant == variant._subject) {
                    item = items[i];
                    break;
                }
            }
            //If this item variant isn't already in the cart add it
            if(!item) {
                item = new CartItemVM(self, product, variant);
                
                self.data().sus_items.push(item);
                self.data().sus_lineitem_nextId++;
            }
            item.sus_quantity(parseInt(item.sus_quantity()) + 1);
            item.view_quantity(item.sus_quantity());

            self.save();
        }

        self.deleteLineitem = function(item){
            self.data().sus_items.remove(item);
            self.save();
        }

        self.deleteCart = function() {
            ld_util.send_delete(self.cartUrl, function(response){
                ld_util.get(self.cartUrl, self.loadResponseData);
            })
        }

        self.save = function(){

            var cart = self.data();
            var modCount = cart.ce_modificationCount;

            //convert observable sus_items to simple array
            cart.sus_items = cart.sus_items();
            //convert observable quantity to primitive            
            for(i=cart.sus_items.length-1;i>=0;i--){
                cart.sus_items[i].sus_quantity = cart.sus_items[i].view_quantity();
                if(cart.sus_items[i].sus_quantity < 1) {
                    cart.sus_items.splice(i,1);
                }
            }
            var cartPatch = cart.make_patch();

            ld_util.send_patch(self.cartUrl, modCount, cartPatch, function(request){
                if(request.responseXML)
                    self.loadResponseData(request);
                else
                    ld_util.get(self.cartUrl,self.loadResponseData);
            });
        }

        self.loadResponseData = function(response) {
            var savedCart = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(response);
            if(!savedCart.sus_items)
                savedCart.sus_items = []
            //Make quantity observable and add computed function for lineitem_price
            for(i=0;i<savedCart.sus_items.length;i++){
                savedCart.sus_items[i] = new CartItemVM(self, savedCart.sus_items[i]);
            }
            //make items an observable array
            savedCart.sus_items = ko.observableArray(savedCart.sus_items);
            self.data(savedCart);
        }

        ko.postbox.subscribe("active_view", function(message) {
            if (message.view == 'cart') {
                self.showView();
                document.title = 'Cart';
            }
            else {
                self.hideView();
                //revert any unsaved quantity changes 
                var items = self.data().sus_items();
                for(i=0;i<items.length;i++){
                    items[i].view_quantity(items[i].sus_quantity());
                }
                self.data().sus_items(items);
            }
        }, true);

        return self;
    }