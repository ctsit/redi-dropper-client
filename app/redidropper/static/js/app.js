
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
    var container = $("#redcap_subjects_container");
    container.empty();

    var thead = $('<thead><tr> <th> # </th> <th> Name </th> <th> Number of Files </th> </tr>'); 
    var tbody = $('<tbody>');
    var table = $('<table border="1" cellpadding="2" cellspacing="2" id="redcap_subjects">').append(thead).append(tbody);
    container.append(table);

    var data = {};
    var request = api_request("/api/list_redcap_subjects", "POST", data, "json", true);

    request.success( function(json) {
        console.log(json);
        if (array_keys(json).length < 1) {
            console.log("Empty list returned.");
            return;
        }

        $.each(json, function (i, obj) {
            var row = $('<tr>');
            row.append($('<td>').text(i));
            row.append($('<td>').text(obj.name));
            row.append($('<td>').text(obj.files));
            tbody.append(row);
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
