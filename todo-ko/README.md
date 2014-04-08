# Building an LDA Application Using KnockoutJS

[KnockoutJS](http://knockoutjs.com) is a JavaScript library that helps you to create rich, responsive display and editor user interfaces with a clean underlying data model. Any time you have sections of UI that update dynamically (e.g., changing depending on the user’s actions or when an external data source changes), KO can help you implement it more simply and maintainably. [1](http://knockoutjs.com/documentation/introduction.html)

KnockoutJS ("KO") has four essential features that help with building LDA UIs:

1. Declarative Bindings - Easily associate DOM elements with model data using a concise, readable syntax
2. Automatic UI Refresh - When your data model's state changes, your UI updates automatically
3. Dependency Tracking - Implicitly set up chains of relationships between model data, to transform and combine it
4. Templating - Quickly generate sophisticated, nested UIs as a function of your model data

We like KnockoutJS because it is relatively easy to learn, popular (enough) within the Javascript community, and really focuses on one thing -- data binding the UI to a data model. Unlike Bootstrap, Angular, and Ember, Knockout is not a "full stack" framework. We see this as an advantage compared to the (relatively) heavy weight nature of Ember and Angular. We have little experience with Bootstrap but the experience we do have showed that we didn't use the Bootstrap Controller or Model classes in their intended way.

So while Knockout is fourth in popularity behind Bootstrap, Ember, and Angular in our experience it's "just right" for building a responsive LDA user experience.

## To Do-KO vs The Original To Do

There are two main differences between the original To Do application() and the Knockout version:

1. The original todo app does not maintain a data model. The list is physically in the DOM.
2. The javascript code in the original todo app generates HTML in order to manipulate the todo list.

For a small application neither of these are bad things. As applications get larger and more complex though things can tend toward spaghetti code if there isn't a better separation of concerns between the data and the view. The Javascript community has embraced variations of the MVC pattern to address this (within the community they call these MV* frameworks since a web application rarely implements MVC exactly).

## Learning More About KnockoutJS

Knockout implements the "Model-View-ViewModel" (MVVM) variant of MVC. There are excellent tutorials and documentation to help you learn the basics of Knockout. See http://learn.knockoutjs.com for an interactive tutorial that will teach you all you need to know for our todo app.

## The todo-ko Application

todo-ko uses application.js to bootstrap itself just like the original todo application. We based the look of todo-ko on the popular Twitter Bootstrap CSS/javascript library.

```html
<!-- bootstrap -->
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">
<link rel="stylesheet" href="/todo/style.css">
```

The top of the list.html contains the `link` tags needed to load Bootstrap and our custom CSS file. Because we are using HTML5 it is perfectly permissable to use a `link` tag in the HTML body.

At the end of `list.html` are the javascript includes:

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
<script src="http://cdnjs.cloudflare.com/ajax/libs/knockout/3.1.0/knockout-min.js"></script>
<script type="text/javascript" src="/todo/app.js"></script>
```

We load jQuery (required for Bootstrap), Bootstrap, and Knockout using CDNs. We load the todo application code last.

### Data Binding

We won't dissect the `list.html` HTML line by line but it is useful to highlight an example of Knockout data binding:

```html
<div style="padding-top: 20px;">
    <div class="list-group" data-bind="foreach: items">
        <a class="list-group-item" data-bind="text: title, attr: {href: url}"></a>
    </div>
</div>
```

This code snippets binds the div of class "list-group" to the `items` collection. `items` is an attribute of the ViewModel and is an array. The `data-bind=` syntax is the way to association an HTML element with a ViewModel attribute. For the class we are executing a loop with the `foreach` binding. In the anchor tag we are using both a `text` binding and an `attr` binding to provide the href attribute and the link text from a specific item.

### Binding The ViewModel and The View

In Knockout the "View" is the DOM. You associate a viewmodel with a DOM node using the `applyBindings` function:

```javscript
ko.applyBindings(new ViewModel(), document.getElementById("todo-app"));
```

Here are are associating a ViewModel instance with the DOM node "todo-app" so that updates to the viewmodel are reflected in the DOM and vice-versa.

### The ViewModel

Our ViewModel consists of a set of data declarations and member functions. Knockout uses the concept of an "observable" to specify a data member that can be bound to a UI element. Changes to the observable are automatically reflect in the UI. Likewise, changes in the UI automatically update the observable.

```javascript
function ViewModel() {
    var self = this;
    self.items = ko.observableArray();
    self.itemToAdd = ko.observable("");

    ...
}
```

Here `items` and `itemToAdd` are both Knockout observables. Observables in Knockout are actually implemented as functions and without something like Javascript ES5's getter/setter syntactic sugar you have to use "()" to get the value of an observable.

The ViewModel acts as the data translation layer between the server and the View (HTML page). It is common for the ViewModel to take server data and put it in a format that is most easily rendered by the UI. In our example LDA is providing resources to us in LDA's version of the RDF/JSON format. The UI however only needs the item title and resource URL so the ViewModel just takes the pieces it needs to maintain the ObservableArray of items:

```javascript
function getItems() {
    var items = APPLICATION_ENVIRON.initial_simple_jso.bp_members
    for (var i in items) {
        appendItem(items[i].dc_title, items[i]._subject);
    }
}
```

Adding a new list item leverages the LDA clientlib to take the item from the ViewModel and POST it to the todo server:

```javascript
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
```



