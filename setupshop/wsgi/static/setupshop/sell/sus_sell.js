;(function() {

// ====================

    function BackOfficeViewModel() {
        var self = this;
        self.store = {
            title: ko.observable(),
            uri: ko.observable()
        };
        self.jwt = misc_util.get_jwt_claims();

        self.jwt = misc_util.get_jwt_claims()
        self.loggedin_account = misc_util.get_jwt_claims();

        self.displayName = function() {
            return self.jwt.disp;
        }

        self.showView = function(viewname) {
            ko.utils.arrayForEach(self.apps, function(app) {
                app.show(app.name == viewname);
            });

            return false;
        }

        self.apps = [];
    }


// ====================

    function DashboardViewModel() {
        this.name = 'dashboard';
        this.visible = ko.observable(false);
        this.donutdata = [
            {label: "Download Sales", value: 12},
            {label: "In-Store Sales", value: 30},
            {label: "Mail-Order Sales", value: 20}
        ];

        this.areadata = [
            {period: '2010 Q1', iphone: 2666, ipad: null, itouch: 2647},
            {period: '2010 Q2', iphone: 2778, ipad: 2294, itouch: 2441},
            {period: '2010 Q3', iphone: 4912, ipad: 1969, itouch: 2501},
            {period: '2010 Q4', iphone: 3767, ipad: 3597, itouch: 5689},
            {period: '2011 Q1', iphone: 6810, ipad: 1914, itouch: 2293},
            {period: '2011 Q2', iphone: 5670, ipad: 4293, itouch: 1881},
            {period: '2011 Q3', iphone: 4820, ipad: 3795, itouch: 1588},
            {period: '2011 Q4', iphone: 15073,ipad: 5967, itouch: 5175},
            {period: '2012 Q1', iphone: 10687,ipad: 4460, itouch: 2028},
            {period: '2012 Q2', iphone: 8432, ipad: 5713, itouch: 1791}
        ];

        this.show = function(shouldShow) {
            this.visible(shouldShow);

            // TODO: replace HTML in view with a custom binding
            $('.datatable').dataTable();
        }
    }

    function OrdersViewModel() {
        this.name = 'orders';
        this.visible = ko.observable(false);
        this.orders = ko.observableArray();

        this.show = function(shouldShow) {
            this.visible(shouldShow);
        }
    }


// ====================

    function appInit(data) {
        var backOfficeVM = new BackOfficeViewModel();
        backOfficeVM.store.title(data.sus_store.dc_title);
        backOfficeVM.store.uri(data.sus_store._subject);
        ko.applyBindings(backOfficeVM, document.getElementById('backoffice-nav'));

        var dashboardVM = new DashboardViewModel();
        backOfficeVM.apps.push(dashboardVM);
        ko.applyBindings(dashboardVM, document.getElementById('page-dashboard'));

        var ordersVM = new OrdersViewModel();
        backOfficeVM.apps.push(ordersVM);
        ko.applyBindings(ordersVM, document.getElementById('page-orders'));

        // initialize productcatalog app module
        backOfficeVM.apps.push(App.productcatalog);
        ko.applyBindings(App.productcatalog, document.getElementById('page-productcatalog'));

        // initialize blog app module
        backOfficeVM.apps.push(App.blogapp);
        ko.applyBindings(App.blogapp, document.getElementById('page-blogapp'));

        // get a reference to the global app object and bind backOffice to it
        App = window.App || {};
        App.backOffice = backOfficeVM;


        // set the dashboard as the active VM. Move this later
        backOfficeVM.showView('dashboard');

        /*
        new DashboardViewModel(),
        new BlogViewModel()
        new OrdersViewModel(),
        new CustomersViewModel(),
        new ProductsViewModel(),
        new CollectionsViewModel(),
        new DiscountsViewModel(),
        new GiftCardsViewModel(),
        new ReportsViewModel(),


        new PagesViewModel(),
        new NavigationViewModel(),
        new ThemesViewModel(),

        new AppsViewModel(),
        new SettingsViewModel()
        */

    }

    function showView(data) {
        var result = true;
        if (data.rdf_type.toString() == SUS+'BackOffice') {
            backOfficeVM.store.title(data.sus_store.dc_title);
            backOfficeVM.store.uri(data.sus_store._subject);
        }
        else {
            result = false;
        }

        return result;

    }

    function get_resource_and_show_view(resource_url, history_tracker) {
        ld_util.get(resource_url, function(request){
            if (request.status==200) {
                var resource_json = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                if (showView(resource_json)) { // resource accepted
                    history_tracker.accept_url()
                    }
                else { // we cannot handle this resource
                    history_tracker.decline_url()
                    }
                }
            else if (request.status==401) {
                window.name = resource_url
                var resource_json = JSON.parse(request.responseText)
                window.location.href = resource_json['http://ibm.com/ce/ns#login-page']
                }
            else {
                console.log( request.status )
                }
            })
        }


    var dispatcher = new misc_util.Dispatcher(
        function(element) { // function is called to decide if this single-page-app claims a click on an element
            var segments = element.pathname.split('/')
            return element.host == window.location.host && segments.length > 1 && segments[1] == 'cat'
            },
        get_resource_and_show_view) // function is called a) if a user click is claimed b) if a history event happens c) go_to is called on the dispatcher
    dispatcher.hook_history_and_links();


    var data = APPLICATION_ENVIRON.initial_simple_jso
    appInit(data);
}());

