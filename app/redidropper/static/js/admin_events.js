
function api_request(url, reqType, data, dataType, doCache) {
    return $.ajax({
        url: url,
        type: reqType,
        data: data,
        dataType: dataType,
        cache: doCache
    });
}

function get_subject_files(i) {
    var data ={
        no_of_pages: 10,
        list_of_events: [
            {file_id:"1", file_name:"test 1", file_size:"20th Jan 2015"},
            {file_id:"2",file_name:"test 2",file_size:"3rd Aug 2015"},
            {file_id:"3",file_name:"test 3434",file_size:"1st Dec 2015"}
        ]
    };

    var page_data = {
        list_of_events: [
            {file_id:"3", file_name: "page 2", file_size: "20th Jan 2013"},
            {file_id:"9", file_name: "page 2", file_size:"19th Feb 2015"},
            {file_id:"3",file_name:"page 2",file_size:"2nd Nov 2015"}
        ]
    };

    if (i == 1) {
        return data;
    }
    return page_data;
}

var AdminEventsTable = React.createClass({
  getInitialState: function() {
    return {list_of_events:this.props.list_of_events};
  },
  componentWillReceiveProps:function(nextProps){
       this.setState({list_of_events:nextProps.list_of_events});
  },
  render: function() {
    return (
    <div className="table-responsive" >
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>Event Name</th>
                    <th>Username</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {this.state.list_of_events.map(function(record,i) {
                    return <tr>
                                <td>{record.file_id}</td>
                                <td>{record.file_name}</td>
                                <td>{record.file_size}</td>
                            </tr>
                })}
            </tbody>
        </table>
    </div>
    );
  }
});
var AdminEventsPagination =React.createClass({
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

var AdminEventsList = React.createClass({
  getInitialState: function() {
    return {list_of_events:undefined,no_of_pages:0};
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
    var data = get_subject_files(1);
    this.setState({list_of_events:data.list_of_events,no_of_pages:data.no_of_pages});

  },
  changePage:function(page_no) {
    var data = get_subject_files(page_no);
    this.setState({list_of_events:data.list_of_events,no_of_pages:this.state.no_of_pages});
  },
  render: function() {
    var no_of_pages=this.state.no_of_pages;
    var list_of_events=this.state.list_of_events;
    var pagination;
    if(no_of_pages>1) {
        pagination=<AdminEventsPagination no_of_pages={no_of_pages} changePage={this.changePage}/>;
    }
    var events_table;
    if(list_of_events==undefined) {
        //so some loading screen
    }
    else if(list_of_events.length == 0) {
        events_table=<div>No data to display</div>;
    }
    else {
        events_table=<AdminEventsTable list_of_events={this.state.list_of_events}/>
    }
    return (
    <div>
        {events_table}
        {pagination}
    </div>
    );
  }
});

React.render(<AdminEventsList/>, document.getElementById("admin-events-list"));
