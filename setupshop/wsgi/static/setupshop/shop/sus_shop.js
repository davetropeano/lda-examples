define(['jquery', 'sammy', 'knockout', 'ko_es5', 'ko_amd', 'ko_postbox', 'hover'], function($, Sammy, ko) {
    RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    DC = 'http://purl.org/dc/terms/'
    CE = 'http://ibm.com/ce/ns#'
    SUS = 'http://setupshop.me/ns#'

    function showView(data) {
        var return_code = true;

        if (data.rdf_type.toString() == SUS+'Category') {
            ko.postbox.publish("active_view", {view: "category", data: data});
        }
        else if (data.rdf_type.toString() == SUS+'ProductDescription') {
            return_code = false;
        }
        else if (data.rdf_type.toString() == SUS+'Product') {
            var copy = ko.toJS(data);
            delete copy.rdf_isDefinedBy.sus_describes;

            ko.postbox.publish("active_view", {view: "product", data: copy});
        }
        else if (data.rdf_type.toString() == SUS+'OnlineStore') {
            ko.postbox.publish("active_view", {view: "store", data: data});
        }
        else if (data.rdf_type.toString() == SUS+'BackOffice') {
            window.location = data._subject;
        }
        else {
            return_code = false;
        }

        return return_code;
    };

    return function() {
        var initialLoad = true

        // initialize the application
        var sammy = Sammy(function() {
            this.get('/.*', function() {
                if (this.path == '/cart') {
                    ko.postbox.publish("active_view", {view: 'cart', data: {} });
                }
                else {
                    if (initialLoad) {
                        var data = APPLICATION_ENVIRON.initial_simple_jso
                        if (data.rdf_type.toString() != SUS+'OnlineStore') {
                            ld_util.get('/', function(request){
                                if (request.status==200) {
                                    var store = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                                    ko.postbox.publish("init_header", {data: store});
                                }
                                else {
                                    console.log( request.status )
                                }
                            })
                        }
                        showView(data)
                        initialLoad = false
                    }
                    else {
                        ld_util.get(this.path, function(request){
                            if (request.status==200) {
                                var data = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                                showView(data);
                            }
                            else {
                                console.log( request.status )
                            }
                        });
                    }
                }
            });
        });

        sammy.run();
    };
})

