
// @TODO: move to a separate "utils" class
function array_keys(obj) {
    list = [];
    for (var key in obj) {
        list.push(key);
    }
    return list;
}

function render_subject_files() {
    var data = {"subject_id": "1"};
    var request = api_request("/api/list_subject_files", "POST", data, "json", true);
}

function render_redcap_subjects() {
    var data = {};
    var request = api_request("/api/list_redcap_subjects", "POST", data, "json", true);
    request.success( function(json) {
        console.log(json);
        if (array_keys(json).length < 1) {
            $("#no-table-data-error").text("There are no subject present")
            return;
        }

        $("#technician-table").show();
        $.each(json, function (i, obj) {
            var row = $('<tr>');
            row.append($('<td>').text(obj.id));
            row.append($('<td>').text(obj.name));
            row.append($('<td>').text(obj.files));
            row.append($('<td>').html('<a href="/users/upload/'+obj.id+'" class="btn btn-primary btn">Add</a>'));
            $("#technician-table-body").append(row);
        });
    });

    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
}


function api_request(url, reqType, data, dataType, doCache) {
    return $.ajax({
        url: url,
        type: reqType,
        data: data,
        dataType: dataType,
        cache: doCache
    });
}

function init() {
    // helper or invoking all necessary pieces of code
    render_redcap_subjects();
}


$(document).ready( function() {
    console.log("hello world");
    init();
});
