
function getListOfSubjects(){
    var data =[{subject_id:123,subject_name:"ab"},
              {subject_id:123,subject_name:"abc"},
              {subject_id:123,subject_name:"abc1"},
              {subject_id:123,subject_name:"abc12"},
              {subject_id:123,subject_name:"abc123"},
              {subject_id:123,subject_name:"abc1234"},
              {subject_id:123,subject_name:"abc12345"},
              {subject_id:123,subject_name:"abc123456"}];

    return data;          
}



var SubjectsList = React.createClass({
  getInitialState: function() {
    return {list_of_subjects:[]};
  },
  componentWillMount:function(){
    this.updateSubjectsList('');
  },
  updateSubjectsList:function(subject_name){
    var _this=this;
    var url= "/api/find_subject";
    
    var request = Utils.api_request(url,"POST",{name:subject_name}, "json", true);
    request.success( function(json) {
       _this.setState({list_of_subjects:json.data});
    });
    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
    });
    
  },
  subjectChanged: function() {
    var subject_name= this.refs.subject_name.getDOMNode().value.trim();
    
    if(subject_name.length>2){

        this.updateSubjectsList(subject_name);       
    
    }
    
  },
  render: function() {
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
                {this.state.list_of_subjects.map(function(record,i) {
                    return <tr>
                                <td>{i+1}</td>
                                <td>{record}</td>
                            </tr>           
                })}
            </tbody>
        </table>
    </div>
    </div>
    );
  }
});

React.render(<SubjectsList/>, document.getElementById("subjects-list"));
