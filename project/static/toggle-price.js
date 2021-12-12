window.addEventListener('load', function(){
  const price_switch = document.getElementById("cPriceSwitch");
  
  if(price_switch){
    price_switch.addEventListener('change', togglePriceDisplay);
    function togglePriceDisplay(){
      if (price_switch.checked){
        console.log('toggle price display on')
      }
      else{
        console.log('toggle price display off')
      }
      fetch("/toggle-price-display", {method:'PATCH'})
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    };
  };
})