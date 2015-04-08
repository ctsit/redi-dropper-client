var Utils ={

api_request:function(url, reqType, data, dataType, doCache) {
    return $.ajax({
        url: url,
        type: reqType,
        data: data,
        dataType: dataType,
        cache: doCache
    });
},
array_keys:function (obj) {
    list = [];
    for (var key in obj) {
        list.push(key);
    }
    return list;
}

}