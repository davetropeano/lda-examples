var gc = {} || window.gc;
gc.url_entrypoint = 'http://localhost:3007/items';

$(document).on('pagecreate', "#index", function() {
    route(gc.url_entrypoint);
});

$('#detail-page').on('pageshow', function(event) {
    $('#item-detail').text(JSON.stringify(gc.data, null, 4));
});

$('#submit-button').on('click', postItem);

// $(document).on('click', showItem);
function showItem(elem) {
    console.log(elem);
    // route(this.href);
}

function postItem() {
    var newitem = $('#new-item').val();
    var thedata = {
        "": {"http://purl.org/dc/terms/title": newitem, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://example.org/todo#Item"}
        };
    console.log(newitem);
    $.ajax({
      type: "POST",
      url: gc.url_entrypoint,
      headers: {'CE-Post-Reason': 'CE-Create'},
      data: JSON.stringify(thedata),
      success: handlePostSuccess,
      contentType: 'application/rdf+json+ce'
    });
}

function handlePostSuccess(response) {
    var subject = response[gc.url_entrypoint]['http://www.w3.org/2000/01/rdf-schema#member'].value;
    var title = response[subject]['http://purl.org/dc/terms/title'];
    appendList({"dc_title": title, "subject": subject});
    $('#todo-list').listview("refresh");
}

function loadList() {
    var items = gc.data.rdfs_member;
    items.forEach(appendList);

    $('#todo-list a').on('click', function(event) {
        event.preventDefault();
        route(this.href);
    });

    $('#todo-list').listview("refresh");
}

function appendList(item) {
    item.dc_title = item.dc_title.trim();
    if (item.dc_title) {
        $('#todo-list').append("<li><a href='" + item._subject + "'>" + item.dc_title + "</a></li>");
    }
}

function route(url) {
    $.getJSON(url, function(data) {
        if (typeof data.rdf_type == "object")
            data.rdf_type = data.rdf_type.value;

        gc.data = data;
        if (~data.rdf_type.indexOf('basicProfile#Container'))
            loadList();
        else if (typeof data.rdf_type == "string" && ~data.rdf_type.indexOf('todo#Item'))
            $.mobile.changePage('#detail-page');
        else
            console.log(data);
    });
}