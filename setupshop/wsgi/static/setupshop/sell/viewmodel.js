"use strict";

// Crockford Compositional Inheritence pattern.
// http://javascriptissexy.com/oop-in-javascript-what-you-need-to-know/
if (typeof Object.create !== 'function') {
    Object.create = function (o) {
        function F() {
        }

        F.prototype = o;
        return new F();
    };
}

function inheritPrototype(childObject, parentObject) {
    var copyOfParent = Object.create(parentObject.prototype);

    copyOfParent.constructor = childObject;
    childObject.prototype = copyOfParent;
}

// --------------------------------------

function ViewModel(name) {
    this.name = name;
    this.visible = ko.observable(false);
    this.views = [];
    this.currentView = ko.observable(false);
    this.defaultView = '';
}

ViewModel.prototype = {
    constructor: ViewModel,

    show: function(shouldShow) {
        var self = this;

        if (shouldShow == true) {
            self.showDefaultView();
            self.visible(true);
        }
        else {
            self.visible(false);
            ko.utils.arrayForEach(self.views, function(view) {
                view.visible(false);
            });
        }
    },

    showDefaultView: function() {
        this.showView(this.defaultView);
    },

    showView: function(viewname) {
        var self = this;
        self.currentView(); // clear the current view

        ko.utils.arrayForEach(self.views, function(view) {
            if (view.name == viewname) {
                view.visible(true);
                self.currentView(viewname);
            }
            else
                view.visible(false);
        });
    },

    addView: function(viewname) {
        this.views.push({name: viewname, visible: ko.observable(false)});
    }
};
