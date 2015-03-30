
// @TODO: move to a separate "utils" class

function render_subject_files() {
    var data = {"subject_id": "1"};
    var request = api_request("/api/list_subject_files", "POST", data, "json", true);
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

function getProjectsList(){
    return [{project_id:"1",project_name:"1st Project"},{project_id:"2",project_name:"2nd Project"}]
}

var SubjectsTable = React.createClass({
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

var Technician = React.createClass({
  getInitialState: function() {
    return {projects: [],selected_project:0,error:[]};
  },
  componentWillMount:function(){
    /*
    var request = api_request("/api/list_redcap_subjects", "POST", data, "json", true);
    request.success( function(json) {
        this.setState({projects:json,selected_project:json[0].id});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
    */
  },
  selectChanged:function(){
    console.log("select changed "+this.refs.project_select.getDOMNode().value);
    var new_selected_value = this.refs.project_select.getDOMNode().value;
    this.setState({projects:this.state.projects,selected_project:new_selected_value});
  },
  render: function() {

    return (
    <div>
    <div className="row">
        <div className="col-sm-4">
            <h3> Project Name </h3>
        </div>
        <div className="col-sm-4">
            <select onChange={this.selectChanged}  className="form-control" ref="project_select">
                {this.state.projects.map(function(record,i) {
                        return <option value={record.project_name}>{record.project_name}</option>           
                })};  
            </select>
        </div>
        <div className="col-sm-4">
        </div>
    </div>
        <br/>
        <h3>List of Subjects </h3>
        <br/>
        <SubjectsTable selected_project={this.state.selected_project}/>
    </div>
    );
  }
});


React.render(<Technician/>, document.getElementById("technician"));
