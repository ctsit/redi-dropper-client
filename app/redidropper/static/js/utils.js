var Utils = {

api_request: function(url, reqType, data, dataType, doCache) {
    return $.ajax({
        url: url,
        type: reqType,
        data: data,
        dataType: dataType,
        cache: doCache
    });
},

api_post_json: function(url, data) {
    return Utils.api_request(url, 'POST', data, 'json', true);
},

array_keys: function (obj) {
    list = [];
    for (var key in obj) {
        list.push(key);
    }
    return list;
},

validateEmail: function(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

}
