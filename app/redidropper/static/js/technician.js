// @TODO: add description

var SubjectsRow = React.createClass({
    getInitialState: function() {
        return {
            row_data: this.props.row_data, 
            max_events: this.props.max_events
        };
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState(
                {
                    row_data: nextProps.row_data,
                    max_events: nextProps.max_events
                });
    },
    showAlert: function() {
        $("#event-alert").show();
        setTimeout(function () {
            $("#event-alert").hide();
        }, 1500)
    },
    render: function() {
        var column_count = this.state.max_events;
        var table_columns = [];
        var row_data = this.state.row_data;
        var events_count=row_data.events.length;

        for(var i = 0; i < events_count; i++) {
            var view_files_url = "/users/manage_event/"+row_data.events[i].event_id;
            if (row_data.events[i].event_files != 0) {
                table_columns.push(<td><a href={view_files_url}>{row_data.events[i].event_files}</a></td>);
            }
            else {
                table_columns.push(<td><a href={view_files_url}><i className="fa fa-lg fa-plus-circle"></i></a></td>);
            }
        }
        var view_files_url="/users/manage_event/new";
        table_columns.push(<td><a href={view_files_url}><i className="fa fa-lg fa-plus-circle"></i></a></td>);

        for (var i = events_count + 2; i <= column_count; i++) {
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
        return {
            subjects: [],
            max_events: this.props.max_events,
            no_of_pages:0
        };
    },
    changePage: function(i) {
        this.changeData(i, this.state.max_events)
    },
    changeData: function(page_num, max_events) {
        // if needed we will allow the user to select how many rows to display per page
        var per_page = 10
        var data = {'per_page': per_page, 'page_num': page_num}

        var _this = this;
        var request = Utils.api_post_json("/api/list_of_subjects", data);
        request.success( function(json) {
            _this.setState({
                subjects: json.list_of_subjects,
                max_events: max_events,
                no_of_pages: json.total_pages
            });
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },
    componentWillMount: function() {
        this.changeData(1, this.props.max_events);
    },
    componentWillReceiveProps: function(nextProps) {
        this.changeData(1, nextProps.max_events);
    },
    render: function() { 
        var table_rows = [];
        var subjects_data = this.state.subjects;
        var row_count = subjects_data.length;
        var column_count = this.state.max_events;

        for(var i = 0; i < row_count; i++) {
            table_rows.push(<SubjectsRow row_data={subjects_data[i]} max_events={column_count}/>);
        }

        var table_columns = [];

        if (row_count != 0) {
            table_columns.push(<th>Subject ID</th>);
            table_columns.push(<th>Name</th>);
            for (var i = 1; i <= column_count; i++) {
                table_columns.push(<th> Event {i}</th>);
            }
        }
        var pagination ;
        var no_of_pages = this.state.no_of_pages;

        if (no_of_pages !=1 || no_of_pages != 0) {
            pagination = <SubjectsPagination no_of_pages={no_of_pages} changePage={this.changePage}/>;
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
  componentWillReceiveProps: function(nextProps) {
    this.setState({no_of_pages:nextProps.no_of_pages,current_page:this.state.current_page});
  },
  activateOnClick: function(i) {
    this.setState({no_of_pages:this.state.no_of_pages,current_page:i});
    this.props.changePage(i);
  },
  nextPage: function() {
    var current_page=this.state.current_page;
    if(current_page==this.state.no_of_pages) {
        return;
    }
    else {
        this.setState({no_of_pages:this.state.no_of_pages,current_page:current_page+1});
        this.props.changePage(current_page+1);
    }
  },
  prevPage: function() {
    var current_page = this.state.current_page;
    if(current_page == 1) {
        return;
    }
    else {
        this.setState({no_of_pages:this.state.no_of_pages,current_page:current_page-1});
        this.props.changePage(current_page-1);
    }
  },
  render: function() {
    var pages = [];
  
    for(var i = 1; i <= this.state.no_of_pages; i++) {
        if(i == this.state.current_page) {
            pages.push(<li className="active"><a>{i}</a></li>);
        }
        else {
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
        // return {projects:[],selected_project:undefined,max_events:0};
        return {max_events: 0};
    },
    componentWillMount: function() {
        /*
        var _this = this;
        var request = Utils.api_request("/api/list_of_projects", "GET",{}, "json", true);
        request.success( function(json) {
            _this.setState({
                max_events: json.max_events
            });
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
        */
    },
    selectChanged: function() {
        /*
        console.log("select changed "+this.refs.project_select.getDOMNode().value);
        var new_selected_value = this.refs.project_select.getDOMNode().value;
        this.setState({ects,selected_project:new_selected_value});
        */
    },
    changePage: function() {

    },
    render: function() {
        /*
        <div className="col-sm-4">
            <select onChange={this.selectChanged}  className="form-control" ref="project_select">
                {this.state.projects.map(function(record,i) {
                        return <option value={record.project_name}>{record.project_name}</option>
                })};
            </select>
        </div>
        */
    return (
    <div>
    <div className="row">
        <div className="col-sm-4">
            <h3> Project: ADRC </h3>
        </div>
        <div className="col-sm-4">
        </div>
    </div>
        <br/>
        <h3>List of Subjects </h3>
        <br/>
        <SubjectsTable max_events={this.state.max_events}/>
    </div>
    );
  }
});

React.render(<Technician/>, document.getElementById("technician"));
