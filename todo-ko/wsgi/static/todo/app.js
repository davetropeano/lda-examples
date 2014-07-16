function ViewModel() {
    var self = this;
    self.items = ko.observableArray();
    self.itemToAdd = ko.observable("");

    self.addItem = function() {
        var title = self.itemToAdd().trim();
        if (title == '') return;

        var item = {
            _subject: "",
            "dc_title": title,
            rdf_type: "http://example.org/todo#Item"
        };

        var response = ld_util.send_create("", item);
        if (response.status == 201) {
            var location = response.getResponseHeader("location");
            appendItem(title, location);

            self.itemToAdd("");
        }
        else
            console.log(response);
    }

    function appendItem(title, url) {
        self.items.push({title: title, url: url});
    }

    function getItems() {
        var items = APPLICATION_ENVIRON.initial_simple_jso.ldp_contains
        if (items)
            for (var i in items) {
                appendItem(items[i].dc_title, items[i]._subject);
            }
    }

    getItems();
}

ko.applyBindings(new ViewModel(), document.getElementById("todo-app"));