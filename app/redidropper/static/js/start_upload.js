// Components used:
//
//      __3 FilesUpload
//      __4 NavController

// var Utils, React, $;

var FilesUpload = React.createClass({

    componentWillMount: function() {
        var self = this;
        var resumable = Utils.get_resumable_instance();

        resumable.on('complete', function() {
            console.log("Uploaded byte count: " + resumable.getSize());
            $("#upload-complete-button").show();
        });

        resumable.on('uploadStart', function() {
            $("#upload-complete-button").hide();
        });
    },
    render: function() {
        return (
                <div className="table-responsive" >
                </div>
               );
    }
});


// ============ __4 NavController
var NavController = React.createClass({
    render: function() {
        $("#upload-files").hide();
        $("#upload-complete-button").hide();

        window.location.hash = 'Files';
        $("#upload-files").show();
        $("#files-list").empty();

        // pass data to Resumable object so we can map files to the subject
        var visible_tab = <FilesUpload showFiles = {this.showFiles}
        />;

        return (
            <div>
                <div className="panel-body">
                    {visible_tab}
                </div>
            </div>
        );
    }
});

React.render(<NavController/>, document.getElementById("start-upload"));
