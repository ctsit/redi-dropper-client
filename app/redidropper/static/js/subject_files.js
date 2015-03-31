function api_request(url, reqType, data, dataType, doCache) {
    return $.ajax({
        url: url,
        type: reqType,
        data: data,
        dataType: dataType,
        cache: doCache
    });
}

function get_subject_files(){
    var data =[{foldername:"Folder 1",list_of_files:[{file_id:"1",file_name:"test 1",file_size:"10MB"},{file_id:"1",file_name:"test 2",file_size:"20MB"},{file_id:"3",file_name:"test 3434",file_size:"30MB"}]},
                {foldername:"Folder 2",list_of_files:[{file_id:"2",file_name:"test 1",file_size:"10MB"},{file_id:"1",file_name:"test 2",file_size:"20MB"},{file_id:"3",file_name:"test 3434",file_size:"30MB"}]},
                {foldername:"Folder 3",list_of_files:[{file_id:"3",file_name:"test 1",file_size:"10MB"},{file_id:"1",file_name:"test 2",file_size:"20MB"},{file_id:"3",file_name:"test 3434",file_size:"30MB"}]},
                {foldername:"Folder 4",list_of_files:[{file_id:"4",file_name:"test 1",file_size:"10MB"},{file_id:"1",file_name:"test 2",file_size:"20MB"},{file_id:"3",file_name:"test 3434",file_size:"30MB"}]}
                ];
     return data;           
}

var FolderFilesList = React.createClass({
  getInitialState: function() {
    return {list_of_files:this.props.list_of_files,visibility:this.props.visibility};
  },
  componentWillReceiveProps:function(nextProps){
        this.setState({list_of_files:nextProps.list_of_files,visibility:nextProps.visibility});
  },
  render: function() {
    var style={};
    if (!this.state.visibility) {
        style.display = 'none';
    }
    return (    
    <div className="table-responsive" style={style}>
        <div>{this.props.selected_project}</div>
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
                    var add_url="/users/file_download/"+record.id;
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

var FoldersList = React.createClass({
  getInitialState: function() {
    var data = get_subject_files();
    for( var i=0;i<data.length;i++){
        data[i].visible=false;
    }
    return {subjects:data};
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
  collapseAll:function(){
    var data=this.state.subjects;
    for( var i=0;i<data.length;i++){
        data[i].visible=false;
    }
     this.setState({subjects:data});
  },
  displayAll:function(){
    var data=this.state.subjects;
    for( var i=0;i<data.length;i++){
        data[i].visible=true;
    }
     this.setState({subjects:data});
  },
  changeDisplay:function(i){
    var data=this.state.subjects;
    data[i].visible=!(data[i].visible);
    this.setState({subjects:data});
  },
  render: function() {
    var _this=this;
    return (
    <div>
    <button onClick={this.collapseAll} className="btn btn-primary btn">Collapse All</button>
    <button onClick={this.displayAll} className="btn btn-primary btn">Display All</button>
        {this.state.subjects.map(function(record,i) {
            return <div>
                    <h3 onClick={_this.changeDisplay.bind(null,i)}>{record.foldername}</h3>
                    <br></br>
                    <FolderFilesList folder_id={record.foldername} list_of_files={record.list_of_files} visibility={record.visible}/>  
                    </div>                        
        })}
    </div>
    );
  }
});


React.render(<FoldersList/>, document.getElementById("subject-files-list"));