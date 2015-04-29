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

// ============ __1 SubjectsList
var SubjectsList = React.createClass({
    getInitialState: function() {
        return {
            list_of_subjects: []
        };
    },

    componentWillMount: function() {
        // this.updateSubjectsList('');
    },

    updateSubjectsList: function(subject_name) {
        var _this = this;
        var url = "/api/find_subject";
        var request = Utils.api_post_json(url, {name: subject_name});
        request.success( function(json) {
            _this.setState({
                list_of_subjects: json.data.subjects
            });
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },

  subjectChanged: function() {
    var subject_name = this.refs.subject_name.getDOMNode().value.trim();
    if (subject_name.length > 0) {
        this.updateSubjectsList(subject_name);
    }
  },

  render: function() {
    var rows = [];
    var _this = this;

    this.state.list_of_subjects.map(function(record, i) {
        // Wire the click on the button to the parent
        // function subjectSelected() with the parameter record
        // which allows the parent component to access record data
        var selectSubject = _this.props.subjectSelected.bind(null, record);
        rows.push(
            <tr>
                <td>
                    <button className="btn btn-lg2 btn-primary btn-block"
                        onClick={selectSubject}>
                        {record}
                        </button>
                </td>
              </tr>
        );
    });

    return (
    <div>

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
       _this.setState({
           list_of_events: json.data.events
       });
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render: function() {
    var rows = [];
    var _this = this;
    this.state.list_of_events.map(function(record, i) {
        var callback = _this.props.eventSelected.bind(null, record);
        var event_name = record.unique_event_name;

        rows.push(
            <tr>
                <td>
                    <button className="btn btn-lg2 btn-primary btn-block"
                        onClick={callback}>
                        {event_name}
                    </button>
                </td>
            </tr>
        );
    });

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
    var request_data = { 'subject_id': '1', 'event_id': '2'};
    var request = Utils.api_post_json("/api/list_subject_event_files", request_data);
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


// ============ __0 NavController
var NavController = React.createClass({
    getInitialState: function() {
        //Add Listner for the url change
        window.onhashchange = this.urlChanged;

        var tabs = [
            "Subjects",
            "Events",
            "Files"
        ];
        return {
            current_tab: 0,
            tabs: tabs,
            subject_id: "",
            event_id: ""
        };
    },
    changeTab: function(i) {
        this.setState({
          current_tab: i
        }); 
 
        if (0 === i) {
          this.setState({
            event_id: ""
          });
        }
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
      if("#"+this.state.tabs[current_tab] !== hash_value) {
        //State has to be changed
        if(hash_value === "#Subjects") {
          this.setState({current_tab: 0,event_id:""});
        }
        else if (hash_value === "#Events" && this.state.current_tab === 2) {
          // The condition 'this.state.current_tab==2' is to avoid
          // state changes for forward button click from subjects tab
          this.setState({current_tab: 1});
        }
      }
    },
    render: function() {
        var visible_tab;
        var selected_subject_id;
        var selected_event_id;
        var breadcrumbs = [];
        var current_tab = this.state.current_tab;
        var tabs = this.state.tabs;

        if(this.state.subject_id !== "") {
            selected_subject_id = "Subject ID: " + this.state.subject_id;
        }
        if(this.state.event_id !== "") {
            selected_event_id = "Event: " + this.state.event_id.unique_event_name;
        }

        for(var i = 0; i < tabs.length; i++) {
            var tab_class;
            if(current_tab === i) {
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

        if(current_tab === 0) {
            window.location.hash = 'Subjects';
            //By Passing the Subject selected function to the SubjectsList component
            //We are allowing the SubjectsList component to execute it when 
            // it is time to change the visible tab
            visible_tab = <SubjectsList subjectSelected = {this.subjectSelected}/>;
        }
        else if(current_tab === 1) {
            window.location.hash = 'Events';
            visible_tab = <EventsList eventSelected = {this.eventSelected}/>;
        }
        else if(current_tab === 2) {
            window.location.hash = 'Files';
            $("#upload-files").show();
            $("#files-list").empty();
            visible_tab = <FilesUpload showFiles = {this.showFiles}/>;
        }

        return (
            <div>
                <div className="panel-heading">
                    <div id="crumbs">
                        <ul>
                            {breadcrumbs}
                        </ul>
                    </div>
                </div>
                <div className="row">
                <div className="col-md-offset-4 col-md-4 col-xs-12">
                <table id="technician-table" className="table table-striped">
                    <thead>
                    <tr>
                        <th>{selected_subject_id}</th>
                        <th>{selected_event_id}</th>
                     </tr>
                </thead>
                </table>
                </div>
                </div>
                <div className="panel-body">
                    {visible_tab}
                </div>
            </div>
        );
    }
});

React.render(<NavController/>, document.getElementById("start-upload"));
