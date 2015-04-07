
// @TODO: move to a separate "utils" class
function array_keys(obj) {
    list = [];
    for (var key in obj) {
        list.push(key);
    }
    return list;
}

function render_redcap_users() {
    var data = {};
    var request = api_request("/api/list_redcap_subjects", "POST", data, "json", true);
    request.success( function(json) {
        console.log(json);
        if (array_keys(json).length < 1) {
            $("#no-table-data-error").text("There are Users Present")
            return;
        }
        $("#admin-table").show();
        json=[{id:"123",username:"test1",email:"test1@gmail.com",date_added:"20th Jan",role:"admin",email_verified:"1"},
              {id:"546",username:"test2",email:"test2@gmail.com",date_added:"10th Jan",role:"technician",email_verified:"0"},
              {id:"897",username:"test3",email:"test3@gmail.com",date_added:"10th Jan",role:"researcher",email_verified:"0"}];
        $.each(json, function (i, obj) {
            var row = $('<tr>');
            row.append($('<td>').text(obj.id));
            row.append($('<td>').text(obj.username));
            row.append($('<td>').text(obj.email));
            row.append($('<td>').text(obj.role));
            row.append($('<td>').text(obj.date_added));
            if(obj.email_verified=="1"){
                row.append($('<td>').text("Yes"));
            }else{
                row.append($('<td>').html('<button class="btn btn-primary btn">Send Verification Email</button>'));
            }
            row.append($('<td>').html('<button class="btn btn-primary btn user-update">Update</button>   <button class="btn btn-primary btn">Remove</button>'));            
            $("#admin-table-body").append(row);
        });
        add_events_to_new_data();
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
    render_redcap_users();
}

function add_events_to_new_data(){
    $(".user-update").unbind( "click" );
    $(".user-update").on('click',function(e){
        var current = $(this).text();
        console.log(current+" "+$(this).text());
        if(current=="Update"){
            $(this).text("Save");
        }else if(current=="Save"){
            $(this).text("Update");
        }
    });
}

$("#admin-save").click(function(){
    var username = $("#admin-add-username").val();
    var email = $("#admin-add-email").val();
    var role = $("#admin-add-role").val();

    //Generate a post request and get the new object details

    var row = $('<tr>');
    row.append($('<td>').text("20"));
    row.append($('<td>').text(username));
    row.append($('<td>').text(email));
    row.append($('<td>').text(role));
    row.append($('<td>').text("30th Jan"));
    row.append($('<td>').html('<button class="btn btn-primary btn">Send Verification Email</button>'));        
    row.append($('<td>').html('<button class="btn btn-primary btn user-update">Update</button>   <button class="btn btn-primary btn">Remove</button>'));            
    $("#admin-table-body").append(row);
    add_events_to_new_data();
});



$(document).ready( function() {
    init();
});
