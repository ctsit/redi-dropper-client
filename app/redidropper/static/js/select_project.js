var ProjectsTable = React.createClass({
  getInitialState: function() {
    return {list_of_projects:this.props.list_of_projects};
  },
  componentWillReceiveProps:function(nextProps){
       this.setState({list_of_projects:nextProps.list_of_projects});
  },
  render: function() {
    return (
    <div className="table-responsive" >
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>Project Id</th>
                    <th>Project Name</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {this.state.list_of_projects.map(function(record,i) {
                    var redirect_url = "/set_project"+record.project_id;
                    var button=<a href={redirect_url} className="btn btn-default">Select</a>
                    return <tr>
                                <td>{record.project_id}</td>
                                <td>{record.project_name}</td>
                                <td>{button}</td>
                            </tr>
                })}
            </tbody>
        </table>
    </div>
    );
  }
});

var ProjectsList = React.createClass({
  getInitialState: function() {
    return {list_of_projects:undefined};
  },
  componentWillMount:function(){
    var _this=this;
    var request = Utils.api_request("/api/list_of_projects", "GET", {}, "json", true);
    request.success( function(json) {
       _this.setState({list_of_projects:json.list_of_projects});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render: function() {
    var list_of_projects=this.state.list_of_projects;
    var projects_table;
    if(list_of_projects==undefined) {
        //so some loading screen
    }
    else if(list_of_projects.length == 0) {
        projects_table=<div>No data to display</div>;
    }
    else {
        projects_table=<ProjectsTable list_of_projects={this.state.list_of_projects}/>
    }
    return (
    <div>
        {projects_table}
    </div>
    );
  }
});

React.render(<ProjectsList/>, document.getElementById("projects-list"));