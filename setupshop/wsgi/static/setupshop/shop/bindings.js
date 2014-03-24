define(['knockout'], function(ko) {
    ko.bindingHandlers.dollars = {
        update: function(element, valueAccessor) {
            var value = ko.utils.unwrapObservable(valueAccessor()),
                formattedValue = (value/100).toFixed(2);

                ko.bindingHandlers.text.update(element, function () {
                         return "$ " + formattedValue;
                });
        }
    };
})