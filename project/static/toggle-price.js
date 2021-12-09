const price_switch = document.getElementById("cPriceSwitch");
// const current_url= window.location.host ;

price_switch.addEventListener('change', togglePriceDisplay)
function togglePriceDisplay(){

  if (price_switch.checked){
    console.log('toggle on')
  }
  else{
    console.log('toggle off')
  }
  fetch("/toggle-price-display", {method:'PATCH'})
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

