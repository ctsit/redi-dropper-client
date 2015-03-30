function api_request(url, reqType, data, dataType, doCache) {
    return $.ajax({
        url: url,
        type: reqType,
        data: data,
        dataType: dataType,
        cache: doCache
    });
}

var SubjectFilesList = React.createClass({
  getInitialState: function() {
    return {subjects:[]};
  },
  componentWillMount:function(){
    var request = api_request("/api/list_redcap_subjects", "POST",{}, "json", true);
    var _this=this;
    request.success( function(json) {
        console.log("success "+json);
        _this.setState({subjects:json});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render: function() {
    return (
    <div className="table-responsive">
        <div>{this.props.selected_project}</div>
        <table id="technician-table" className="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>No. of Files</th>
                    <th></th>
                </tr>
            </thead>
            <tbody id="technician-table-body">
                {this.state.subjects.map(function(record,i) {
                    
                    var add_url="/users/upload/"+record.id;
                    var file_url="/users/project/"+record.id+"/subject/"+record.id;
                    return <tr>
                                <td>{record.id}</td>
                                <td>{record.name}</td>
                                <td><a href={file_url} className="btn btn-primary btn">{record.files}</a></td>
                                <td><a href={add_url} className="btn btn-primary btn">Add</a></td>
                            </tr>           
                })}
            </tbody>
        </table>
    </div>
    );
  }
});


React.render(<SubjectFilesList/>, document.getElementById("subject-files-list"));