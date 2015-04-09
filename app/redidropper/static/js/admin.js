var AdminUsersTable = React.createClass({
  getInitialState: function() {
    return {list_of_users:this.props.list_of_users};
  },
  componentWillReceiveProps:function(nextProps){
       this.setState({list_of_users:nextProps.list_of_users});
  },
  render: function() {
    return (    
    <div className="table-responsive" >
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Date Added</th>
                    <th>Email Verified</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {this.state.list_of_users.map(function(record,i) {
                    var email;
                    if(record.email_verified==0){
                        email=<div>Verified</div>;
                    }else if(record.email_verified==1){
                        email=<button className="btn btn-primary btn">Send Verification Email</button>;
                    }
                    
                    return <tr>
                                <td>{record.id}</td>
                                <td>{record.username}</td>
                                <td>{record.email}</td>
                                <td>{record.role}</td>
                                <td>{record.date_added}</td>
                                <td>{email}</td>
                                <td><button className="btn btn-primary btn user-update">Update</button>   <button className="btn btn-primary btn">Remove</button></td>
                            </tr>           
                })}
            </tbody>
        </table>
    </div>
    );
  }
});

var AdminUsersPagination =React.createClass({
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


var AddNewUserForm = React.createClass({
  addUser:function(){
    //Get the values entered by the user in the form
    var user_email = this.refs.user_email.getDOMNode().value.trim();    
    var user_first_name = this.refs.user_first_name.getDOMNode().value.trim();
    var user_middle_name = this.refs.user_middle_name.getDOMNode().value.trim();
    var user_last_name = this.refs.user_last_name.getDOMNode().value.trim();
    var user_role = this.refs.user_role.getDOMNode().value.trim();

    var data={  user_email      :  user_email,
                user_first_name :  user_first_name,
                user_middle_name:  user_middle_name,
                user_last_name  :  user_last_name,
                user_role       :  user_role };

    var request = Utils.api_request("/api/save_user", "POST",data, "json", true);
    
    var _this=this;
    
    request.success( function(json) {
        console.log('Response add user: ' + JSON.stringify(json));
    });

    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  render:function(){

    return (  
    <div className="col-sm-5">
    <h3> Add New User </h3>
    <br/>
        <div className="form-horizontal">
         <div className="form-group">
            <label for="inputEmail3" className="col-sm-4 control-label">Email</label>
            <div className="col-sm-8">
              <input type="email" className="form-control" ref="user_email" placeholder="Email"/>
            </div>
          </div>
          <div className="form-group">
            <label for="inputEmail3" className="col-sm-4 control-label">First Name</label>
            <div className="col-sm-8">
              <input type="text" className="form-control" ref="user_first_name" placeholder="First Name"/>
            </div>
          </div>
          <div className="form-group">
            <label for="inputEmail3" className="col-sm-4 control-label">Middle Name</label>
            <div className="col-sm-8">
              <input type="text" className="form-control" ref="user_middle_name" placeholder="Middle Name"/>
            </div>
          </div>
          <div className="form-group">
            <label for="inputEmail3" className="col-sm-4 control-label">Last Name</label>
            <div className="col-sm-8">
              <input type="text" className="form-control" ref="user_last_name" placeholder="Last Name"/>
            </div>
          </div>
          <div className="form-group">
            <label for="inputEmail3" className="col-sm-4 control-label">Role</label>
            <div className="col-sm-8">
              <select ref="user_role" className="form-control">
                  <option value="admin">Admin</option>
                  <option value="technician">Technician</option>
                  <option value="researcher">Researcher</option>
                </select>
            </div>
          </div>
          <div className="form-group">
            <div className="col-sm-offset-2 col-sm-10">
              <button onClick={this.addUser} className="btn btn-primary btn">Add User to Project</button>
            </div>
          </div>
        </div>
    </div>
    )
  }

});

var AdminUserManagement = React.createClass({
  getInitialState: function() {
    return {list_of_users:undefined,no_of_pages:10,show_user_form:false};
  },
  componentWillMount:function(){
    var request = Utils.api_request("/api/users/list", "GET", {}, "json", true);
    var _this=this;
    request.success( function(json) {
        _this.setState({list_of_users:json.users,no_of_pages:10});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },
  changePage:function(page_no){
  },
  toggleAddUserForm:function(){
    //change the bool value of show_user_form variable to opposite 
    var show_user_form =!this.state.show_user_form;
    this.setState({list_of_users    :  this.state.list_of_users,
                    no_of_pages     :  this.state.no_of_pages,
                    show_user_form  :  show_user_form});
  },
  render: function() {
    var no_of_pages=this.state.no_of_pages;
    var list_of_users=this.state.list_of_users;
    var pagination;
    var show_user_form;
    var button_text="Add User";
    if(no_of_pages>1){
        pagination=<AdminUsersPagination no_of_pages={no_of_pages} changePage={this.changePage}/>;
    }
    if(this.state.show_user_form){
      button_text="Close";
      show_user_form=<AddNewUserForm onSubmit={this.addNewUser}/>
    }
    var users_table;
    if(list_of_users==undefined){
        //show some loading screen
    }else if(list_of_users.length==0){
        users_table=<div>No data to display</div>;
    }else{
        users_table=<AdminUsersTable list_of_users={this.state.list_of_users}/> 
    }
    return (  
    <div>
    <button onClick={this.toggleAddUserForm} className="btn btn-primary">{button_text}</button>
    <br/>
    {show_user_form}
    {users_table}
    {pagination}
    </div>
    );
  }
});
React.render(<AdminUserManagement/>, document.getElementById("admin-user-managememt"));