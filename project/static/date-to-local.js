window.addEventListener('load', function () {
  // Have to append the 'Z' at the end so js parses as UTC
  const dCreated = new Date(document.getElementById('date-created').innerText+'Z');
  const dModified = new Date(document.getElementById('date-modified').innerText+'Z');
  document.getElementById('date-created').innerText = dCreated.toLocaleString()
  document.getElementById('date-modified').innerText = dModified.toLocaleString()
})