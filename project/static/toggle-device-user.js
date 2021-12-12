window.addEventListener('load', function(){
  console.log('Script User')
  const user_switches = this.document.querySelectorAll('.switch-device-user');
  
  if(user_switches){
    user_switches.forEach(function(item){
      item.addEventListener('change', function(){
        const device = item.getAttribute('id').replace('user_','')
        if (item.checked){
          console.log(`Toggle ${device} on`)
        }
        else{
          console.log(`Toggle ${device} off`)
        }
        fetch(`/toggle-user-device/${device}`, {method:'PATCH'})
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
      });
    });
  };
})