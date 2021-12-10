$('#modalDelete').on('show.bs.modal', function(e) {
  var deviceId = $(e.relatedTarget).data('device-id');
  var deviceName = $(e.relatedTarget).data('device-name');
  var myUrl = `/delete-device/${deviceId}`;
  $(e.currentTarget).find('span[name="deviceName"]').text(deviceName);
  $('#btnModalDelete').click(function(){    
    console.log(`Trying to delete device ${deviceId}`);
    $.ajax({
      url:myUrl,
      type:"DELETE",
      success: function(result){
        console.log(`Deleted device ${deviceId}`);
        console.log(result)
        $('#modalDelete').modal('toggle');   
        location.reload();
      },
      error:function(error){
        console.log(error)
      }
    });
  });
});


