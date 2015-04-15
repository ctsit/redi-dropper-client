// Implements react componenst:
//  AdminUsersTable - ...
//  AdminUsersPagination - ..
//  AddNewUserForm - ...

var AdminUsersTable = React.createClass({
  getInitialState: function() {
    return {list_of_users:this.props.list_of_users};
  },
  componentWillReceiveProps: function(nextProps) {
       this.setState({list_of_users: nextProps.list_of_users});
  },
  render: function() {
    return (
    <div className="table-responsive" >
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>First name</th>
                    <th>Last name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Date Added</th>
                    <th>Email Verified</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {this.state.list_of_users.map(function(record,i) {
                    var emailButton;

                    if(record.email_verified == 1) {
                        emailButton = <div>Verified</div>;
                    }
                    else if (record.email_verified == 0) {
                        emailButton = <button className="btn btn-primary btn">Send Verification Email</button>;
                    }
                    var active;
                    if(record.usrIsActive) {
                        active = <button className="btn btn-primary btn">Activate</button>;
                    }
                    else {
                        active = <button className="btn btn-primary btn">Deactivate</button>;
                    }
                    return <tr>
                                <td>{record.usrID}</td>
                                <td>{record.uathUsername}</td>
                                <td>{record.usrFirst}</td>
                                <td>{record.usrLast}</td>
                                <td>{record.usrEmail}</td>
                                <td>{record.rolName}</td>
                                <td>{record.usrAddedAt[0]}</td>
                                <td>{emailButton}</td>
                                <td>{active}</td>
                            </tr>
                })}
            </tbody>
        </table>
    </div>
    );
  }
});

var AdminUsersPagination = React.createClass({
  getInitialState: function() {
    return {total_pages:this.props.total_pages, current_page:1};
  },
  componentWillReceiveProps: function(nextProps) {
       //
  },
  activateOnClick: function(i) {
    this.setState({total_pages: this.state.total_pages, current_page: i});
    this.props.changePage(i);
  },
  nextPage: function() {
    var current_page = this.state.current_page;
    if(current_page == this.state.total_pages) {
        return;
    }
    else {
        this.setState({total_pages: this.state.total_pages, current_page: current_page + 1});
        this.props.changePage(current_page + 1);
    }
  },
  prevPage: function() {
    var current_page=this.state.current_page;
    if(current_page==1) {
        return;
    }
    else {
        this.setState({total_pages: this.state.total_pages, current_page: current_page - 1});
        this.props.changePage(current_page - 1);
    }
  },
  render: function() {
    var pages=[];
    for(var i=1;i<=this.state.total_pages;i++) {
        if(i==this.state.current_page) {
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


var AddNewUserForm = React.createClass({
  getInitialState: function() {
    return {error:""};
  },
  clearError: function() {
    this.setState({error:""});
  },
  addUser: function() {
    //Get the values entered by the user in the form
    var uathUsername    = this.refs.username.getDOMNode().value.trim();
    var usrEmail        = this.refs.user_email.getDOMNode().value.trim();
    var usrFirst        = this.refs.user_first_name.getDOMNode().value.trim();
    var usrMI           = this.refs.user_middle_name.getDOMNode().value.trim();
    var usrLast         = this.refs.user_last_name.getDOMNode().value.trim();
    var rolName         = this.refs.user_role.getDOMNode().value.trim();

    if (uathUsername.length < 6) {
      this.setState({error:"Username cannot be less than 6 characters."});
      return;
    }

    if (usrEmail == "") {
      this.setState({error:"Email cannot be empty."});
      return;
    }

    if(! Utils.validateEmail(usrEmail)) {
      this.setState({error:"Invalid email address."});
      return;
    }
    if (usrFirst == "") {
      this.setState({error:"First name cannot be empty."});
      return;
    }
    if (usrLast == "") {
      this.setState({error:"Last name cannot be empty."});
      return;
    }
    if (usrMI.length > 1) {
      this.setState({error:"Middle name should be one character long."});
      return;
    }

    if (rolName == "") {
      this.setState({error:"Please select a role for this user."});
      return;
    }

    var data = {
                "uathUsername":  uathUsername,
                "usrEmail"    :  usrEmail,
                "usrFirst"    :  usrFirst,
                "usrMI"       :  usrMI,
                "usrLast"     :  usrLast,
                "rolName"     :  rolName
    };

    console.log('send: ' + data)
    var request = Utils.api_post_json("/api/save_user", data);
    var _this = this;

    request.success( function(json) {
        console.log("got back: " + JSON.stringify(json));

        if(json.status == "success") {
            var record = json.data;
            if (record) {
                var data = {
                    'id'          : record.usrID,
                    'username'    : record.uarhUsername,
                    'email'       : record.usrEmail,
                    'date_added'  : '',
                    'role'        : record.rolName,
                    'email_verified':'0'
                };
                _this.props.addNewUser(data);
            }
        }
        else {
            _this.setState({error:json.message});
            return;
        }
    });

    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
        _this.setState({error:"There was some unknown error.Try Again"});
        return;
    });
  },
  render: function() {
    var error;
    if (this.state.error!="") {
      error=<div className="alert alert-danger alert-dismissible">
              <button type="button" onClick={this.clearError} className="close">&times;</button>
              {this.state.error}
            </div>
    }
    return (
    <div className="col-sm-5">
    <h3> Add New User </h3>
    <br/>
    {error}
        <div className="form-horizontal">
        <div className="form-group">
            <label for="inputEmail3" className="col-sm-4 control-label">Username</label>
            <div className="col-sm-8">
              <input type="text" className="form-control" ref="username" placeholder="username"/>
            </div>
          </div>
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
                  <option value="">Select a Role</option>
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
    return {
        list_of_users: undefined,
        total_pages: 10,
        show_user_form: false,
        error:"",
    };
  },
  componentWillMount: function() {
    var request = Utils.api_post_json("/api/list_users", {'per_page': "10"});
    var _this = this;

    request.success( function(json) {
      if (json.status == "success") {
        _this.setState({list_of_users: json.data});
      }
      else {
        _this.setState({
            list_of_users   :  [],
            total_pages     :  this.state.total_pages,
            show_user_form  :  false,
            error           :  json.message
        });
      }
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
  },

  changePage: function(pageNum) {
    console.log('Goto page: ' + pageNum);
  },

  addNewUser: function(data) {
    var list_of_users = this.state.list_of_users;
    list_of_users.unshift(data);
    this.setState({
        list_of_users   :  list_of_users,
        total_pages     :  this.state.total_pages,
        show_user_form  :  false
    });
  },
  toggleAddUserForm: function() {
    //change the bool value of show_user_form variable to opposite
    var show_user_form = !this.state.show_user_form;
    this.setState({
        list_of_users   :  this.state.list_of_users,
        total_pages     :  this.state.total_pages,
        show_user_form  :  show_user_form
    });
  },
  render: function() {
    var total_pages = this.state.total_pages;
    var list_of_users=this.state.list_of_users;
    var pagination;
    var show_user_form;
    var button_text = "Add User";

    if(total_pages > 1) {
        pagination = <AdminUsersPagination total_pages={total_pages} changePage={this.changePage}/>;
    }

    if(this.state.show_user_form) {
      button_text="Close";
      show_user_form=<AddNewUserForm addNewUser={this.addNewUser}/>
    }

    var users_table;

    if(list_of_users == undefined) {
        //show some loading screen
    }
    else if(this.state.error!="") {
      users_table = <div className="alert alert-danger">Error : {this.state.error} .
                                                         Refresh the page</div>
    }
    else if (0 == list_of_users.length) {
        users_table = <div>No data to display</div>;
    }
    else {
        users_table = <AdminUsersTable list_of_users={this.state.list_of_users}/>
    }
    return (
    <div>
        <button onClick={this.toggleAddUserForm} className="btn btn-primary">{button_text}</button>
        <br/>
        <div className="row">
          {show_user_form}
        </div>
        <div className="row">
          <br/>
          {users_table}
          {pagination}
        </div>
    </div>
    );
  }
});
React.render(<AdminUserManagement/>, document.getElementById("admin-user-managememt"));
