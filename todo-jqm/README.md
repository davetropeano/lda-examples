# Todo jQM - Building A Simple Mobile App With LDA

## Introduction
The todo-jqm sample builds a hybrid mobile application using the [jQueryMobile](http://jquerymobile.com) framework. There are a number of instructive differences between todo-jqm and the original [todo sample](http://github.com/ld4apps/lda-examples/todo):

* CSS styling - todo-jqm uses the jQueryMobile "A" theme.
* No LDA bootstraping - todo-jqm does not use an application.js file to bootstrap itself. Because a mobile application is a separate binary compile todo-jqm is built as a standalone web application that accesses a todo-server through REST.
* No clientlib - for this application sample we chose to not use the clientlib. The LDA clientlib provides a default router and a set of convenience methods for converting to/from our version of JSON (rdf+json+ce). We thought it instructive to expose what a front end developer would have to do *without* clientlib if they wanted to build an application.

## index.html
Because our mobile application is a separate build, the architecture of the app is rooted in an index.html just like any other web applications. We use the basic [jQueryMobile boilerplate](http://demos.jquerymobile.com/1.4.2/pages/) in todo-jqm in the header to load the necessary CSS sheets and libraries.

Unlike many other javascript frameworks, jQM does enhancement on the DOM adding/removing styles and DOM elements to acheive it's look and behaviors. Because of this, you want the jQM javascript files loaded as early as possible. This is in contrast with modern javascript best practices where it is more common to put the javascript loads just about the `</body>` tag in order to allow the browser to do progressive rendering.

```html
<head>
    <title>LDA Todo Mobile</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="/css/jquery.mobile-1.4.2.min.css" />
    <script src="/vendor/jquery-1.9.1.min.js"></script>
    <script src="/vendor/jquery.mobile-1.4.2.min.js"></script>
</head>
```

Mobile screens are called "pages" in jQM. Pages can be implemented within a single HTML file or in separate HTML files. jQM manages loading pages into and out of the DOM dynamically. You can control this at confiugration time but the default is to load and leave the pages in the DOM and use CSS's display attribute to control which page is active. Our application is small and only has two pages. We'll put both pages in the same file (`index.html`) and let jQM manage their loading/unloading by default.

```html
<div data-role="page" id="index">
    <div data-role="header" data-position="fixed">
        <h1>LDA Todo Mobile</h1>
    </div>

    <div role="main" class="ui-content">
        <fieldset class="ui-grid-a">
            <div class="ui-block-a">
                <input id="new-item" placeholder="new todo item...">
            </div>
            <div class="ui-block-b">
                <button data-role="button" data-inline="true" id="submit-button">Add New To Do</button>
            </div>
        </fieldset>

        <ul id="todo-list" data-role="listview" data-inset="true" data-filter="true" data-input="#filter-for-listview">
        </ul>
    </div>

    <div data-role="footer" data-position="fixed">
        <h4><a href="http://davetropeano.github.io/lda">LDA</a></h4>
    </div>
</div>

<div data-role="page" id="detail-page">
    <div data-role="header" data-position="fixed">
        <a href="/" data-role="button" data-icon="carat-l" data-iconpos="notext" data-iconshadow="false" class="ui-icon-alt ui-icon-nodisc">Back</a>
        <h1>LDA Todo Mobile - Details</h1>
    </div>

    <div role="main" class="ui-content">
        <pre id="item-detail"></pre>
    </div>

    <div data-role="footer" data-position="fixed">
        <h4><a href="http://davetropeano.github.io/lda">LDA</a></h4>
    </div>
</div>
```

The HTML code shows two pages -- "index" and "detail-page". Each page has sections for a header, main content area, and footer. These are standard jQM roles. Refer to the jQM documentation on pages for more information.

##todo.js - our application
Because todo-jqm will be running on a phone/tablet it needs an explict URL to access the back end todo server:

```javascript
var URL_ENTRYPOINT = 'http://localhost:3007/items';
```

We bootstrap the application by creating an event which loads the todo list every time a page is created.

```javascript
$(document).on('pagecreate', "#index", function() {
    route(URL_ENTRYPOINT);
});
```

jQueryMobile uses the `on pagecreate` event signal that a page has been loaded into the DOM but not enhanced yet by jQM. The code above is saying that when the index page is created, call the router to get the list of todos.

### The Router

Our router is pretty straightforward. It does a JSON get of the URL requested and then inspects the rdf type in the response. Based on the type it renders a specific page. Since we only have two pages -- a list and a detail page -- a simple `if` check works.

```javascript
function route(url) {
    $.getJSON(url, function(data) {
        if (typeof data.rdf_type == "object")
            data.rdf_type = data.rdf_type.value;

        app.data = data;
        if (~data.rdf_type.indexOf('basicProfile#Container'))
            loadList();
        else if (typeof data.rdf_type == "string" && ~data.rdf_type.indexOf('todo#Item'))
            $.mobile.changePage('#detail-page');
        else
            console.log(data);
    });
}
```

The `if` check is there because the todo server returns data in `rdf+json+ce` format and lists and individual items have slightly different JSON representations as to where the `rdf_type` attribute is stored. This is the kind of functionality the clientlib gives us for "free".

If we get back a container (i.e. an RDF/JSON `BasicProfileContainer`) then we have the list of items and we call the `loadList()` function.

If we get back an item (i.e. an RDF/JSON `todo#Item`) then we change pages to show the detail page.

### Showing the ToDo List

The code for `loadList()` is pretty straight forward -- iterate through the array of items and inject each one into the DOM with the call to `appendList()`. In the todo app we inject an HTML list element with a link to the Item resource URL. Once all the list elements have been added we need to tell jQueryMobile to enhance their styles so we trigger a refresh event on the todo list.

```javascript
function loadList() {
    var items = window.app.data.rdfs_member;
    items.forEach(appendList);

    ...

    $('#todo-list').listview("refresh");
}
```

Because this is a mobile application and not a web page we also have to trap all the anchor text links in the list.

```javascript
function loadList()
    ...

    $('#todo-list a').on('click', function(event) {
        event.preventDefault();
        route(this.href);
    });

    ...
```

Without this when a user tapped one of the items in the list the browser app would open up because the URL is not part of the mobile app's compiled pages (and is fully qualified).

### POSTing New ToDo Items

Adding items to the list is a little complicated using the standard jQuery / jQueryMobile AJAX functions. One reason is because the todo server -- and all LDA servers -- use `rdf+json+ce` as the content type. The jQuery JSON functions only understand `application/json` as a content type. The other reason is because of the required format for the request payload:

```javascript
function postItem() {
    var newitem = $('#new-item').val();
    var thedata = {
        "": {"http://purl.org/dc/terms/title": newitem, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://example.org/todo#Item"}
        };

    $.ajax({
      type: "POST",
      url: URL_ENTRYPOINT,
      headers: {'CE-Post-Reason': 'CE-Create'},
      data: JSON.stringify(thedata),
      success: handlePostSuccess,
      contentType: 'application/rdf+json+ce'
    });
}
```
The jQuery `ajax()` call needs to include a 'CE-Post-Reason' and specific content type in the header. The data has to be formatted in the specific manner for the LDA version of RDF/JSON (rdf+json+ce).

Once the post is made you have to read the RDF/JSON response and parse out the todo item title and resource url. We do this in `handlePostSuccess()`. We parse the respinse and use `appendList()` to add the newly posted todo item to our list.

```javascript
function handlePostSuccess(response) {
    var subject = response[URL_ENTRYPOINT]['http://www.w3.org/2000/01/rdf-schema#member'].value;
    var title = response[subject]['http://purl.org/dc/terms/title'];
    appendList({"dc_title": title, "subject": subject});
    $('#todo-list').listview("refresh");
}
```

The formatting of the post content for consumtion by the server and the handling of the response data format are both things the clientlib helps with alot.

## Wrapping Up

Building a mobile application that accesses LDA resources is pretty straight forward. You treat the LDA resources as an API and build a hybrid application for the mobile application. Routine and request/response parsing can be done by you (not recommended) or by the LDA clientlib (recommended).

The important thing here is that there is no magic. Your mobile application can use whatever libraries and frameworks it wants to create the right experience for your users.

