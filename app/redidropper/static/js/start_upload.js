// Goal: Implement the simple navigation between tabs
//  
//  Subject > Events > Files
//
// Components used:
//
//      __1 SubjectsList
//      __2 EventsList
//      __3 FilesUpload
//      # EventFilesList
//      
//


// ============ __1 SubjectsList
var SubjectsList = React.createClass({
    getInitialState: function() {
        return {
            list_of_subjects: [],
            upload_status: '',
        };
    },

    componentWillMount: function() {
        // this.updateSubjectsList('');
        this.updateUploadStatus();
    },

    updateUploadStatus: function() {
        var upload_count = Utils.getQueryVar('upload_count');
        if (upload_count) {
            var msg = "Success! Total files uploaded: " + upload_count;
            this.setState({
                upload_status: msg
            });
        }
    },
    updateSubjectsList: function(subject_name) {
        var _this = this;
        var url = "/api/find_subject";
        var request = Utils.api_post_json(url, {name: subject_name});
        request.success( function(json) {
            _this.setState({
                list_of_subjects:json.data
            });
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },

  subjectChanged: function() {
    this.updateUploadStatus();
    var subject_name = this.refs.subject_name.getDOMNode().value.trim();
    if (subject_name.length > 0) {
        this.updateSubjectsList(subject_name);
    }
  },

  render: function() {
    var rows = [];
    var _this = this;

    var visible_status;

    if (this.state.upload_status) {
        visible_status = <div className="alert alert-success" role="alert">
            {this.state.upload_status}
        </div>
    }

    {
        this.state.list_of_subjects.map(function(record, i) {
        var callback = _this.props.subjectSelected.bind(null, record);
        rows.push(
            <tr>
                <td>
                    <button className="btn btn-lg2 btn-primary btn-block"
                        onClick={callback}>
                        {record}
                        </button>
                </td>
              </tr>
        );
    })}

    return (
    <div>
        {visible_status}

    <div className="form-group">
        <input className="form-control"
                ref="subject_name"
                onChange={this.subjectChanged}
                placeholder="Please type a Subject ID"
                type="text" />
    </div>
    <div className="table-responsive" >
        <table id="subject-table" className="table table-striped table-curved">
            <thead>
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

// ============ __2  EventsList
var EventsList = React.createClass({
  getInitialState: function() {
    return {list_of_events: []};
  },
  componentWillMount: function() {
    var _this = this;
    var url = "/api/list_events";
    var request = Utils.api_post_json(url, {subject_id: 'a'});

    request.success( function(json) {
       _this.setState({list_of_events:json.data});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render: function() {
    var rows = [];
    var _this = this;
    {
        this.state.list_of_events.map(function(record, i) {
        var callback = _this.props.eventSelected.bind(null, record);
        rows.push(
            <tr>
                <td>
                    <button className="btn btn-lg2 btn-primary btn-block"
                        onClick={callback}>
                        {record}
                    </button>
                </td>
            </tr>
        );
    })}
    return (
    <div>
    <div className="table-responsive">
        <table id="event-table" className="table table-striped table-curved">
            <thead>
                <tr>
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

/**
// ============ __4 EventFilesList
var EventFilesList = React.createClass({
  getInitialState: function() {
    return {list_of_files:[]};
  },
  componentWillMount: function() {
    var _this = this;

    // @TODO: send subject and event
    var request = Utils.api_request("/api/list_of_files/1", "GET", {}, "json", true);
    request.success( function(json) {
       _this.setState({list_of_files: json.list_of_files});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render: function() {
    return (
    <div className="table-responsive" >
        <table id="technician-table" className="table table-striped table-curved">
            <thead>
                <tr>
                    <th># </th>
                    <th>File Name</th>
                    <th>File Size </th>
                    <th> MD5Sum</th>
                    <th> Date Uploaded </th>
                    <th> Uploader </th>
                    <th></th>
                </tr>
            </thead>
            <tbody id="technician-table-body">
                {this.state.list_of_files.map(function(record, i) {
                    var add_url="/download_file/" + record.id;
                    return <tr>
                                <td>{i+1}</td>
                                <td>{record.file_name}</td>
                                <td>{record.file_size}</td>
                                <td> sum </td>
                                <td> 2015-01-01 </td>
                                <td> Technician 1</td>
                                <td><a href={add_url} className="btn btn-primary btn">Download File</a></td>
                            </tr>
                })}
            </tbody>
        </table>
    </div>
    );
  }
});
*/

// ============ __3 FilesUpload
var FilesUpload = React.createClass({
  getInitialState: function() {
    return {};
  },
  componentWillMount: function() {
    var resumable = Utils.get_resumable_instance();

    resumable.on('complete', function() {
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


// ============ __0 Display
var NavController = React.createClass({
    getInitialState: function() {
        //Add Listner for the url change
        window.onhashchange = this.urlChanged;

        var tabs = [
            "Subjects",
            "Events",
            "Files",
            // "Event Folder"
        ];
        return {
            current_tab: 0,
            tabs: tabs,
            subject_id: "",
            event_id: ""
        };
    },
    changeTab: function(i) {
        this.setState({current_tab: i});
    },
    subjectSelected: function(subject_id) {
        this.setState({current_tab: 1, subject_id: subject_id});
    },
    eventSelected: function(event_id) {
        this.setState({current_tab: 2, event_id: event_id});
    },
    showFiles: function() {
        this.setState({current_tab: 3});
    },
    urlChanged:function (){
      var hash_value=location.hash;
      var current_tab = this.state.current_tab;

      //check whether the current state is not equal to hash value
      if("#"+this.state.tabs[current_tab]!=hash_value){
        //State has to be changed
        if(hash_value=="#Subjects"){
          
          this.setState({current_tab: 0});
        }else if(hash_value=="#Events"&&this.state.current_tab==2){
          //The condition 'this.state.current_tab==2' is to avoid
          //state changes for forward button click from subjects tab
          
          this.setState({current_tab: 1});
        }
      }
    },
    render: function() {
        var visible_tab;
        var selected_subject_id;
        var selected_event_id
        var breadcrumbs = [];
        var current_tab = this.state.current_tab;
        var tabs = this.state.tabs;

        if(this.state.subject_id != "") {
            selected_subject_id = <h3>Selected subject ID: {this.state.subject_id}</h3>;
        }
        if(this.state.event_id != "") {
            selected_event_id = <h3>Selected event ID: {this.state.event_id}</h3>;
        }

        for(var i = 0; i < tabs.length; i++) {
            var tab_class;
            if(current_tab == i) {
                breadcrumbs.push(<li><a>{tabs[i]}</a></li>);
            }
            else if(current_tab > i) {
                breadcrumbs.push(
                        <li className="prev-page" onClick={this.changeTab.bind(null, i)}>
                        <a>{tabs[i]}</a>
                        </li>);
            }
            else if(current_tab < i) {
                breadcrumbs.push(<li className="next-page"><a>{tabs[i]}</a></li>);
            }
        }

        $("#upload-files").hide();
        $("#upload-complete-button").hide();
        
        if(current_tab == 0) {
            window.location.hash = 'Subjects';
            visible_tab = <SubjectsList subjectSelected = {this.subjectSelected}/>;
        }
        else if(current_tab == 1) {

            window.location.hash = 'Events';
            visible_tab = <EventsList eventSelected = {this.eventSelected}/>;
        }
        else if(current_tab == 2) {
            window.location.hash = 'Files';
            $("#upload-files").show();
            visible_tab = <FilesUpload showFiles = {this.showFiles}/>;
        }
        /*
        else if(current_tab == 3) {
            visible_tab = <EventFilesList />;
        }
        */

        return (
            <div>
                <div className="panel-heading">
                    <div id="crumbs">
                        <ul>
                            {breadcrumbs}
                        </ul>
                    </div>
                    {selected_subject_id}
                    {selected_event_id}
                </div>
                <div className="panel-body">
                    {visible_tab}
                </div>
            </div>
        );
    }
});

React.render(<NavController/>, document.getElementById("start-upload"));
