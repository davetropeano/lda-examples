//RDF JSON converter and stuff
var XSD = 'http://www.w3.org/2001/XMLSchema#'
var CE = 'http://ibm.com/ce/ns#'
var multi_valued_properties = [CE+'history', CE+'sites']
var predicate_mappings = {
	'http://setupshop.me/ns#' : 'sus',
	'http://www.w3.org/2000/01/rdf-schema#' : 'rdfs',
	'http://www.w3.org/1999/02/22-rdf-syntax-ns#'  : 'rdf',
	'http://open-services.net/ns/basicProfile#' :   'bp',
	'http://www.w3.org/2001/XMLSchema#' :  'xsd',
	'http://purl.org/dc/terms/' : 'dc',
	'http://ibm.com/ce/ns#' : 'ce',
	'http://www.w3.org/2002/07/owl#' : 'owl',
	'http://ibm.com/ce/ac/ns#' : 'ac' 
}

APPLICATION_ENVIRON = {
    rdf_converter: new rdf_util.Rdf_converter(predicate_mappings)
}

$(document).ready(function() {
    /*
    var cartVM = new CartVM();     
    cartVM.addDummyItem = function() {}
    ko.applyBindings(cartVM);
    */
    
    var asyncs = [];
    
    asyncs.data = "/";    
    asyncs[0] = getJsoResource;
    
    asyncs[1] = function(store, callback){
        asyncs.store = store;
        getJsoResource(store.ce_user.sus_cart, callback);
    }
    
    asyncs[2] = function(cart, callback){
        asyncs.cart = cart;
        //getJsoResource(asyncs.cart.sus_cartItems + "?non-member-properties", callback);
        getJsoResource(asyncs.cart.sus_cartItems, callback);
    }
    
    var cartItem = {
            _subject: "",
            rdf_type: new rdf_util.URI("http://setupshop.me/ns#CartItem"),
            testData: "Cart Item Data"
    }
    cartItem = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(cartItem);
    asyncs[3] = function(cartItems, callback){
        ld_util.send_create(asyncs.cart.sus_cartItems,cartItem,callback);
    }
    
    asyncs[4] = function(cartItem_rdf,callback){
        cartItem = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(cartItem_rdf);
        console.log(cartItem);
        //getJsoResource(cart.sus_cartItems,callback);
        callback();
    }
    
    asyncs[5] = function(data, callback){
        getJsoResource(asyncs.cart.sus_cartItems, callback);
    }
    
    /* 
    asyncs = [];
    //create cart
    var cart = {_subject: "", rdf_type: new rdf_util.URI("http://setupshop.me/ns#Cart")}
    cart = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(cart);
    asyncs[0] = function(data,callback){
        ld_util.send_create("/cart",cart,callback);
    }
    
    //post cartItem to cart/user/cartItems
    asyncs[1] = function(cart_rdf,callback){
        cart = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(cart_rdf);
        console.log(cart);
        ld_util.send_create(cart.sus_cartItems,cartItem,callback);        
    }
    
    asyncs[2] = function(cartItem_rdf,callback){
        cartItem = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(cartItem_rdf);
        console.log(cartItem);
        getJsoResource(cart.sus_cartItems,callback);        
    }
    */
        
    asyncProcessor(asyncs);
        
});

function asyncProcessor(asyncs) {
    var nextCall = asyncs[0];
    asyncs.splice(0,1);    
    if(!nextCall) nextCall = function(){};
    
    function callback(data){
        asyncs.data = data;
        asyncProcessor(asyncs);
    }
    nextCall(asyncs.data, callback);    
}

function getJsoResource(path,callback){
    ld_util.get(path,function(response){
        var resource = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(response);
        console.log(resource);
        callback(resource);
    });
}

