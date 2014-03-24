// <style scoped>@import url("http://code.jquery.com/ui/1.10.0/themes/base/jquery-ui.css")</style>
require.config({
    paths: {
        jquery: "//cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min",

        bootstrap: "//netdna.bootstrapcdn.com/bootstrap/3.0.1/js/bootstrap.min",
        hover: "/setupshop/shop/vendor/twitter-bootstrap-hover-dropdown.min",
        toastr: "//cdnjs.cloudflare.com/ajax/libs/toastr.js/2.0.0/js/toastr.min",

        knockout: "//cdnjs.cloudflare.com/ajax/libs/knockout/3.0.0/knockout-min",
        ko_es5: "/setupshop/shop/vendor/knockout-es5.min",
        ko_amd: "/setupshop/shop/vendor/knockout-amd-helpers.min",
        ko_postbox: "/setupshop/shop/vendor/knockout-postbox.min",

        sammy: "//cdnjs.cloudflare.com/ajax/libs/sammy.js/0.7.4/sammy.min",

        css: "/setupshop/shop/vendor/css",
        text: "/setupshop/shop/vendor/text"
    },

    shim: {
        'ko_es5': ['knockout'],
        'ko_amd': ['knockout'],
        'ko_postbox': ['knockout'],
        'sammy': ["jquery"],
        'bootstrap': ['jquery'],
        'hover': ['jquery', 'bootstrap']
    }
});

var css_deps = [
    'css!//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.0.0/css/bootstrap.min.css',
    'css!//cdnjs.cloudflare.com/ajax/libs/toastr.js/2.0.1/css/toastr.min.css',
    'css!/setupshop/shop/sus_shop.css'];

require(css_deps, function() {
    require(['knockout', '/setupshop/shop/sus_shop.js', 'bootstrap'], function(ko, App) {
        ko.applyBindings({});
        var app = new App();
    });
});
