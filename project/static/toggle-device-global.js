window.addEventListener('load', function(){
  console.log('Script Global')
  const global_switches = this.document.querySelectorAll('.switch-device-global');
  
  if(global_switches){
    global_switches.forEach(function(item){
      item.addEventListener('change', function(){
        const device = item.getAttribute('id').replace('global_','')
        if (item.checked){
          console.log(`Toggle ${device} on`)
        }
        else{
          console.log(`Toggle ${device} off`)
        }
        fetch(`/toggle-default-device/${device}`, {method:'PATCH'})
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
      });
    });
    // console.log('hello')
  };
})