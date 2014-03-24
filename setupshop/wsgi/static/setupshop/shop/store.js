define(function(require) {
    var ko = require('knockout');
    require('ko_es5');
    require('ko_postbox');
    //require('/sitedesign/utils.js');

    var StoreVM = function() {
        var self = this;
        self.jwt = misc_util.get_jwt_claims();
        self.categories = [];
        self.store = null;
        self.visible = false;

        self.showView = function(store) {
            //self.jwt = misc_util.get_jwt_claims()
            self.store = store
            document.title = store.dc_title;

            ld_util.get(store.sus_categories, function(request){
                if (request.status==200) {
                    self.categories = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request).bp_members
                    }
                else {
                    console.log( request.status )
                    }
                })

            self.visible = true;
        };

        self.displayName = function() {
            return self.jwt.disp ? self.jwt.disp : "Guest"
        }
        
        self.loggedIn = function() {
            return self.jwt.acc
        }

        self.login = function() {
            misc_util.get_login()
        }
        
        self.logout = function() {
            misc_util.post_logout()
        }
        
        self.hideView = function() {
            self.visible = false;
        };

        self.initialize = function() {
            ko.postbox.subscribe("active_view", function(message) {
                if (message.view == 'store') {
                    self.showView(message.data);
                }
                else
                    self.hideView();
            }, true);
            ko.postbox.subscribe("init_header", function(message) {
                //self.jwt = misc_util.get_jwt_claims()
                self.store = message.data
            }, true);
        }

        ko.track(this);
    };

    return new StoreVM();

});
