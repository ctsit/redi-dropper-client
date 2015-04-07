
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

function getSubjectsList(){
    return {
        max_events:12,
        subjects_data:
            [
                {subject_id:"1",subject_name:"Subject 1",events:[{event_id:23,event_files:100}]},
                 {subject_id:"2",subject_name:"Subject 2",events:[{event_id:23,event_files:50},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30}]},
                        {subject_id:"3",subject_name:"Subject 3",events:[{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30}]},
                        {subject_id:"4",subject_name:"Subject 4",events:[{event_id:23,event_files:10},{event_id:23,event_files:30},{event_id:23,event_files:30}]},
                        {subject_id:"5",subject_name:"Subject 5",events:[{event_id:23,event_files:16}]},
                        {subject_id:"6",subject_name:"Subject 6",events:[{event_id:23,event_files:18}]}
                        ]};
}

function getNewSubjectsList(){
       return {
        max_events:12,
        subjects_data:
            [
                {subject_id:"7",subject_name:"Subject 7",events:[{event_id:23,event_files:100}]},
                {subject_id:"8",subject_name:"Subject 8",events:[{event_id:23,event_files:50},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30}]},
                {subject_id:"9",subject_name:"Subject 9",events:[{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30},{event_id:23,event_files:30}]},
                {subject_id:"10",subject_name:"Subject 10",events:[{event_id:23,event_files:10},{event_id:23,event_files:30},{event_id:23,event_files:30}]},
                {subject_id:"11",subject_name:"Subject 11",events:[{event_id:23,event_files:16}]},
                {subject_id:"12",subject_name:"Subject 12",events:[{event_id:23,event_files:18}]}
            ]};
}
var SubjectsRow = React.createClass({
  getInitialState: function() {
    return {row_data:this.props.row_data,max_events:this.props.max_events};
  },
  componentWillReceiveProps:function(nextProps){
    this.setState({row_data:nextProps.row_data,max_events:nextProps.max_events});
  },
  showAlert:function(){
    $("#event-alert").show();
    setTimeout(function () {
        $("#event-alert").hide();
    }, 1500)
  },
  render: function() {
    var column_count = this.state.max_events;
    var table_columns=[];
    var row_data=this.state.row_data;
    var events_count=row_data.events.length;
    for(var i=0;i<events_count;i++){
        var view_files_url="/users/manage_event/"+row_data.events[i].event_id;
        if (row_data.events[i].event_files!=0){
            table_columns.push(<td><a href={view_files_url}>{row_data.events[i].event_files}</a></td>);
        }else{
            table_columns.push(<td><a href={view_files_url}><i className="fa fa-lg fa-plus-circle"></i></a></td>);
        }
    }
    var view_files_url="/users/manage_event/new";
    table_columns.push(<td><a href={view_files_url}><i className="fa fa-lg fa-plus-circle"></i></a></td>);
    for(var i=events_count+2;i<=column_count;i++){
        table_columns.push(<td><i className="fa fa-lg fa-plus-circle" onClick={this.showAlert}></i></td>);
    }
    return (
        <tr>
        <td>{row_data.subject_id}</td>
        <td>{row_data.subject_name}</td>
        {table_columns}
        </tr>
    );
}
});


var SubjectsTable = React.createClass({
  getInitialState: function() {
    return {subjects:getSubjectsList()};
  },
  changePage:function(i){
    var data ;
    if(i%2==0){
        data= getSubjectsList();
    }else{
        data= getNewSubjectsList();
    }
    this.setState({subjects:data});
  },
  componentWillMount:function(){
    /*
    var request = api_request("/api/list_redcap_subjects", "POST",{}, "json", true);
    var _this=this;
    request.success( function(json) {
        console.log("success "+json);
        _this.setState({subjects:json});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });*/
  },
  render: function() {
    var column_count = this.state.subjects.max_events;
    var subjects_data=this.state.subjects.subjects_data;
    var row_count = subjects_data.length;
    var table_columns=[];
    table_columns.push(<th>Subject ID</th>);
    table_columns.push(<th>Name</th>);
    for(var i=1;i<=column_count;i++){
        table_columns.push(<th> Event {i}</th>);
    }

    var table_rows= [];
    for(var i=0;i<row_count;i++){
        table_rows.push(<SubjectsRow row_data={subjects_data[i]} max_events={column_count}/>);
    }

    var pagination ;
    var no_of_pages = 10
    if(this.state.subjects.length<3){

    }else{
        pagination=<SubjectsPagination no_of_pages={no_of_pages} changePage={this.changePage}/>;
    
    }
    return (
    <div className="table-responsive">
        <div>{this.props.selected_project}</div>
        <table id="technician-table" className="table table-striped">
            <thead>
                <tr>
                    {table_columns}
                </tr>
            </thead>
            <tbody id="technician-table-body">
                {table_rows}
            </tbody>
        </table>
        {pagination}
    </div>
    );
  }
});

var SubjectsPagination =React.createClass({
  getInitialState: function() {
    return {no_of_pages:this.props.no_of_pages,current_page:1};
  },
  componentWillReceiveProps:function(nextProps){
       // this.setState({list_of_files:nextProps.list_of_files,visibility:nextProps.visibility});
  },
  activateOnClick:function(i){
    this.setState({no_of_pages:this.state.no_of_pages,current_page:i});
    this.props.changePage(i);
  },
  nextPage:function(){
    var current_page=this.state.current_page;
    if(current_page==this.state.no_of_pages){
        return;
    }else{
        this.setState({no_of_pages:this.state.no_of_pages,current_page:current_page+1});
        this.props.changePage(current_page+1);
    }
  },
  prevPage:function(){
    var current_page=this.state.current_page;
    if(current_page==1){
        return;
    }else{
        this.setState({no_of_pages:this.state.no_of_pages,current_page:current_page-1});
        this.props.changePage(current_page-1);
    }
  },
  render: function() {
    var pages=[];
  
    for(var i=1;i<=this.state.no_of_pages;i++){
        if(i==this.state.current_page){
            pages.push(<li className="active"><a>{i}</a></li>);
        }else{
            pages.push(<li><a onClick={this.activateOnClick.bind(null,i)}>{i}</a></li>);
        }
    }
    return (
    <nav>
      <ul className="pagination">
        <li>
          <a onClick={this.prevPage} aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        {pages}
        <li>
          <a onClick={this.nextPage} aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>  
    );
  }
});


var Technician = React.createClass({
  getInitialState: function() {
    return {projects:getProjectsList(),selected_project:0,error:[]};
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
  changePage:function(){

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
