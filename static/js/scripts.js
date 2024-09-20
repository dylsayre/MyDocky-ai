function LoadingSpinner (form, spinnerHTML) {
    form = form || document
  
    //Keep track of button & spinner, so there's only one automatic spinner per form
    var button
    var spinner = document.createElement('div')
    spinner.innerHTML = spinnerHTML
    spinner = spinner.firstChild
  
    //Delegate events to a root element, so you don't need to attach a spinner to each individual button.
    form.addEventListener('click', start)
  
    //Stop automatic spinner if validation prevents submitting the form
    //Invalid event doesn't bubble, so use capture
    form.addEventListener('invalid', stop, true)
  
    //Start spinning only when you click a submit button
    function start (event) {
      if (button) stop()
      button = event.target
      if (button.type === 'submit') {
        LoadingSpinner.start(button, spinner)
      }
    }
  
    function stop () {
      LoadingSpinner.stop(button, spinner)
    }
  
    function destroy () {
      stop()
      form.removeEventListener('click', start)
      form.removeEventListener('invalid', stop, true)
    }
  
    return {start: start, stop: stop, destroy: destroy}
  }
  
  LoadingSpinner.start = function (element, spinner) {
    element.classList.add('loading')
    return element.appendChild(spinner)
  }
  
  LoadingSpinner.stop = function (element, spinner) {
    element.classList.remove('loading')
    return spinner.remove()
  }
  
  
  //Bring your own spinner. You can use any html as the spinner. I'm using just plain text. Maybe technically not a spinner, but this is more about the script than graphics.
  var exampleForm = document.querySelector('#secform')
  var exampleLoader = new LoadingSpinner(secform, 'Sending...')
  exampleForm.addEventListener('submit', LoadingSpinner.start)