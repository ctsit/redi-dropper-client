$( document ).ready(function() {
var r = new Resumable({
  target:'/api/upload',
  chunkSize:10*1024*1024,
  simultaneousUploads:4,
  testChunks:false,
  throttleProgressCallbacks:1
});

// If Resumable.js isn't supported, fall back on a different method
if(!r.support) {
	console.log("Resumable is Not Supported . Switch to Some other Style");
}else{
   console.log("Resumable.js Works");
   r.assignBrowse(document.getElementById('file-select'));
   r.assignDrop(document.getElementById('file-drop'));
   $("#pause-button").hide();
   $("#cancel-button").hide();
   // Handle file add event
   r.on('fileAdded', function(file){
         // Show progress pabr
         $("#file-upload-progress-bar").show();        
         $('#files-list').append('<a href="#" id="file-progress-list-item-'+file.uniqueIdentifier+'" class="file-progress-list-item list-group-item list-group-item-info"><span id="file-status-'+file.uniqueIdentifier+'" class="file-status pull-right">Uploading</span>'+file.fileName+'<span id="file-progress-'+file.uniqueIdentifier+'" class="file-progress-status pull-right">0%</span></a>');
         r.upload();
   });
   r.on('pause', function(){
         $('.file-status').html('Paused');
   });
   r.on('complete', function(){
         // Hide pause/resume when the upload has completed
         $("#pause-button").hide();
         $("#cancel-button").hide();         
         $("#file-upload-progress-bar").hide(); 
   });
   r.on('fileSuccess', function(file,message){
         // Reflect that the file upload has completed
         $('#file-status-'+file.uniqueIdentifier).html('Success');
         $('#file-progress-list-item-'+file.uniqueIdentifier).attr('class','file-progress-list-item list-group-item list-group-item-success');
   });
   r.on('fileError', function(file, message){
         $('#file-status-'+file.uniqueIdentifier).html('Error');
         $('#file-progress-list-item-'+file.uniqueIdentifier).attr('class','file-progress-list-item list-group-item list-group-item-danger');
  
   });
   r.on('fileProgress', function(file){
            // Handle progress for both the file and the overall upload
            $('#file-progress-'+file.uniqueIdentifier).html(Math.floor(file.progress()*100) + '%');
            $('#file-upload-progress').attr('aria-valuenow',r.progress()*100);
            $('#file-upload-progress').css('width', Math.floor(r.progress()*100) + '%');
            $('#file-upload-progress').html(Math.floor(r.progress()*100) + '%');
   });
   r.on('cancel', function(){
         $('.file-progress-status').html('');
         $('.file-status').html('Cancelled');
         $('.file-progress-list-item').attr('class','file-progress-list-item list-group-item list-group-item-danger');
  
   });
   r.on('uploadStart', function(){

            $('.file-status').html('Uploading');
            // Show pause, hide resume
            $("#pause-button").show();
            $("#cancel-button").show();
            $("#files-status").show();
      });
   }

 $("#pause-button").click(function(){
   var currentvalue = $("#pause-button").text();
   if(currentvalue=="Pause"){
      r.pause();
      $("#pause-button").text("Start");
   }else if(currentvalue=="Start"){
      r.upload();
      $("#pause-button").text("Pause");
   }
 });

 $("#cancel-button").click(function(){
   r.cancel();
 });        

 });        
