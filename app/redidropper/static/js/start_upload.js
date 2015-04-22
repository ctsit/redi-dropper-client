// @TODO: document
//
var EventFilesList = React.createClass({
  getInitialState: function() {
    return {list_of_files:[]};
  },
  componentWillMount:function(){
    var _this=this;
    var request = Utils.api_request("/api/list_of_files/1", "GET", {}, "json", true);
    request.success( function(json) {
       _this.setState({list_of_files:json.list_of_files});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render: function() {
    return (    
    <div className="table-responsive" >
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
                {this.state.list_of_files.map(function(record,i) {
                    var add_url="/download_file/"+record.id;
                    return <tr>
                                <td>{record.file_id}</td>
                                <td>{record.file_name}</td>
                                <td>{record.file_size}</td>
                                <td><a href={add_url} className="btn btn-primary btn">Download File</a></td>
                            </tr>           
                })}
            </tbody>
        </table>
    </div>
    );
  }
});

var FilesUpload = React.createClass({
  getInitialState:function(){
    return {show_button:false}
  },
  componentWillMount:function(){
    var _this=this;
    var r = Utils.get_resumable_instance();
    r.on('complete', function() {
       _this.setState({show_button:true});
    });
    r.on('uploadStart', function() {
      if(_this.state.show_button){
        _this.setState({show_button:false});
      }
    });
  },
  render: function() {
    var button;
    if(this.state.show_button){
      button = <button className="btn btn-defualt" 
                       onClick={this.props.showFiles}>
                       Show Files
                </button>;
    }
    return (    
    <div className="table-responsive" >
      {button}
    </div>
    );
  }
});
var EventsList = React.createClass({
  getInitialState: function() {
    return {list_of_events:[]};
  },
  componentWillMount:function(){
    var _this=this;
    var url= "/api/list_events";
    
    var request = Utils.api_post_json(url,{subject_id:'a'});
    request.success( function(json) {
       _this.setState({list_of_events:json.data});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render: function() {
    var rows =[];
    var _this=this;
    {this.state.list_of_events.map(function(record,i) {
        var callback=_this.props.eventSelected.bind(null,record);
        rows.push(<tr>
                    <td>{i+1}</td>
                    <td><button 
                        className="btn white" 
                        onClick={callback}>{record}
                        </button>
                    </td>
                  </tr>
                  );           
    })}
    return (
    <div>  
    <div className="table-responsive" >
        <table id="event-table" className="table table-striped">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Event</th>
                </tr>
            </thead>
            <tbody id="subject-table-body">
                {rows}
            </tbody>
        </table>
    </div>
    </div>
    );
  }
});

var SubjectsList = React.createClass({
  getInitialState: function() {
    return {list_of_subjects:[]};
  },
  componentWillMount:function(){
    this.updateSubjectsList('');
  },
  updateSubjectsList:function(subject_name) {
    var _this=this;
    var url= "/api/find_subject";
    
    var request = Utils.api_post_json(url,{name:subject_name});
    request.success( function(json) {
       _this.setState({list_of_subjects:json.data});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
    
  },
  subjectChanged: function() {
    var subject_name = this.refs.subject_name.getDOMNode().value.trim();
    this.updateSubjectsList(subject_name);       
    if (subject_name.length > 2) { }
  },
  render: function() {
    var rows =[];
    var _this=this;
    {this.state.list_of_subjects.map(function(record,i) {
        var callback=_this.props.subjectSelected.bind(null,record);
        rows.push(<tr>
                    <td>{i+1}</td>
                    <td><button 
                        className="btn white" 
                        onClick={callback}>{record}
                        </button>
                    </td>
                  </tr>
                  );           
    })}

    return (
    <div>
    <div className="form-group ">
        <input className="form-control" 
                ref="subject_name" 
                onChange={this.subjectChanged}
                placeholder="Enter Subject Name" 
                type="text" />
    </div>    
    <div className="table-responsive" >
        <table id="subject-table" className="table table-striped">
            <thead>
                <tr>
                    <th>No</th>
                    <th>RedCap Subject</th>
                </tr>
            </thead>
            <tbody id="subject-table-body">
               {rows}
            </tbody>
        </table>
    </div>
    </div>
    );
  }
});

var Display = React.createClass({
  getInitialState: function() {
    var tabs=["Subjects","Events","Files","Upload Result"];
    return {current_tab:0,tabs:tabs,subject_id:"",event_id:""};
  },
  changeTab:function(i){
    this.setState({current_tab:i})
  },
  subjectSelected:function(subject_id){
    this.setState({current_tab:1,subject_id:subject_id})
  },
  eventSelected:function(event_id){
    this.setState({current_tab:2,event_id:event_id})
  },
  showFiles:function(){
    this.setState({current_tab:3})
  },
  render: function() {
    var display ;
    var subject_id;
    var event_id
    var breadcrumbs=[];
    var current_tab = this.state.current_tab;
    var tabs = this.state.tabs;

    if(this.state.subject_id!=""){
      subject_id = <h3>Subject Id : {this.state.subject_id}</h3>;
    }
    if(this.state.event_id!=""){
      event_id = <h3>Event Id : {this.state.event_id}</h3>;
    }

    for(var i =0 ;i<tabs.length;i++){
      var tab_class;
      if(current_tab==i){
        breadcrumbs.push(<li><a>{tabs[i]}</a></li>);
      }else if(current_tab>i){
        breadcrumbs.push(<li className="prev-page" onClick={this.changeTab.bind(null,i)}>
                              <a>{tabs[i]}</a>
                         </li>);
      }else if(current_tab<i){
        breadcrumbs.push(<li className="next-page"><a>{tabs[i]}</a></li>);
      }
    }

    $("#upload-files").hide();
    if(current_tab==0){
      display = <SubjectsList subjectSelected={this.subjectSelected}/>;
    }else if(current_tab==1){
      display = <EventsList eventSelected={this.eventSelected}/>;
    }else if(current_tab==2){
      $("#upload-files").show();
      display = <FilesUpload showFiles={this.showFiles}/>;
    }else if(current_tab==3){
      display = <EventFilesList />;
    }
    
    return (
    <div>
          <div id="crumbs">
            <ul>
              {breadcrumbs}
            </ul>
          </div>
          <br/>
          <br/>
          {subject_id}
          {event_id}
          {display}
    </div>
    );
  }
});

React.render(<Display/>, document.getElementById("start-upload"));
