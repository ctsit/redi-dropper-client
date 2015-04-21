// @TODO: document
//

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
