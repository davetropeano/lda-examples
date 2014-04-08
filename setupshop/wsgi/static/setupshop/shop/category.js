define(['knockout', 'ko_es5'], function(ko) {
    var CategoryVM = function() {
        var self=this;
        self.products = [];
        self.visible = false;

        self.showView = function(category) {
            ld_util.get(category.sus_categoryProducts, function(request){
                if (request.status==200) {
                    self.products = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request).ldp_contains;
                    document.title = self.products[0].dc_title;
                }
                else {
                    console.log( request.status )
                }
            })

            self.visible = true;
        };

        self.hideView = function() {
            self.visible = false;
        };

        ko.track(this);

        ko.postbox.subscribe("active_view", function(message) {
            if (message.view == 'category') {
                self.showView(message.data);
            }
            else
                self.hideView();
        }, true);
    };

    return new CategoryVM();
})