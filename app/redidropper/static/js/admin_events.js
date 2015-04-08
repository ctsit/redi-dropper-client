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
                                <td>{record.event_id}</td>
                                <td>{record.username}</td>
                                <td>{record.timestamp}</td>
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
    var _this=this;
    var request = Utils.api_request("/api/admin/events/1", "GET", {}, "json", true);
    request.success( function(json) {
       _this.setState({list_of_events:json.list_of_events,no_of_pages:json.no_of_pages});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  changePage:function(page_no) {
    var _this=this;
    var request = Utils.api_request("/api/admin/events/"+page_no, "GET", {}, "json", true);
    request.success( function(json) {
       _this.setState({list_of_events:json.list_of_events,no_of_pages:json.no_of_pages});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
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
