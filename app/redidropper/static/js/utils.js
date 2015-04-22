/* 
* Contains Methods which are used through out the application
* Written in module pattern
* Returns a singleton instance of Resumable Js
*/

var Utils = (function() {

    var resumable_instance;

    function api_request_private(url, reqType, data, dataType, doCache) {
        return $.ajax({
            url: url,
            type: reqType,
            data: data,
            dataType: dataType,
            cache: doCache
        });
    }

    function create_resumable_instance() {
        resumable_instance = new Resumable({
                                target:'/api/upload',
                                chunkSize: 10*1024*1024,
                                simultaneousUploads: 4,
                                testChunks: false,
                                throttleProgressCallbacks: 1,
                                maxFileSize: 1 * 1024 * 1024 * 1024 // 1 GB max
                            });
    }

    function validate_email_private(email) {
        var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        return re.test(email);
    }

    return { 
        // public interface
        api_post_json: function (url,data) {
            return api_request_private(url, 'POST', data, 'json', true);
        },
        api_get_json: function (url,data) {
            return api_request_private(url, 'GET', data, 'json', true);
        },
        api_request:function(url, reqType, data, dataType, doCache){
            return api_request_private(url, reqType, data, dataType, doCache);
        },
        get_resumable_instance:function(){
            if(!resumable_instance){
                create_resumable_instance();
            }
            return resumable_instance;
        },
        validate_email:function(email){
            return validate_email_private(email);
        }
    };

})();


