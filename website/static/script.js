
function parseJavaScriptCode(jsCode) {
  // Parse the JavaScript snippet with Acorn
  const parsedCode = acorn.parse(jsCode, { ecmaVersion: 'latest' });

  // Extract classes, functions, and other code constructs from the parsed code
  const classes = [];
  const functions = [];
  let otherCode = '';

  parsedCode.body.forEach(node => {
      if (node.type === 'ClassDeclaration') {
          const classSnippet = jsCode.substring(node.start, node.end);
          classes.push(classSnippet);
      } else if (node.type === 'FunctionDeclaration') {
          const functionSnippet = jsCode.substring(node.start, node.end);
          functions.push(functionSnippet);
      } else {
          otherCode += jsCode.substring(node.start, node.end);
      }
  });

  return {
      classes: classes,
      functions: functions,
      otherCode: otherCode
  };
}

function toggleEditorTyping(enableTyping) {
  editor.setOption("readOnly", !enableTyping);
}

function hideResultText(){
  document.getElementById('resultsText').style.display='none';
}
function showResultText(){
  document.getElementById('resultsText').style.display='block';
}


function showLoadingSpinner() {
  var loadingSpinner = document.getElementById('loadingSpinner');
  loadingSpinner.style.display = 'block'; // Show the loading spinner
}

function hideLoadingSpinner() {
  var loadingSpinner = document.getElementById('loadingSpinner');
  loadingSpinner.style.display = 'none'; // Hide the loading spinner
}

function showScoreCircle() {
  var scorecirce = document.getElementById('score_circle');
  var graycirce = document.getElementById('gray_circle');
  var percent = document.getElementById('percent');
  scorecirce.style.display = 'block'; // Show the loading spinner
  graycirce.style.display = 'block'; // Show the loading spinner
  percent.style.display='block'
}

function hideScoreCircle() {
  var scorecirce = document.getElementById('score_circle');
  var graycirce = document.getElementById('gray_circle');
  var percent = document.getElementById('percent');
  scorecirce.style.display = 'none'; // Hide the loading spinner
  graycirce.style.display = 'none'; // Hide the loading spinner
  percent.style.display='none';
}


function ratioDisplay(ratio) {
  let percentageText = document.getElementById('percent');
  let counter =0;
  let percentage=Math.round(ratio*100);
  console.log(percentage);
  let totalTime = 200; // Total time in milliseconds (2 seconds)

  let increment = (percentage/ totalTime);
  console.log(increment); // Calculate the increment per 2 seconds

  setTimeout(function() {document.querySelectorAll('#inputButtons button').forEach(button => {
  button.disabled = false;
  showResultText();
  
  toggleEditorTyping(true);
  });}, 2000);
  hideLoadingSpinner();
  showScoreCircle();
// Update the content of the <text> element with the desired percentage value

  let interval=setInterval(()=>{
    if (counter==percentage){
      clearInterval;
    }else{
      counter+=1;
      percentageText.innerHTML =`${counter}%`;
    }

  },2000/percentage)
  var circle = document.getElementById('score_circle');
  let resultText= document.getElementById('resultsText');
  var offset_value=450-450*ratio;
  circle.style.setProperty('--custom-stroke-dashoffset', offset_value);
  if (ratio<0.2){
      circle.style.animation="ringAnimation 2s linear forwards, anim 2s linear forwards";
      resultText.innerHTML =`The code is most-likely self-written`;
      
    }else if(ratio>=0.2&&ratio<0.6){
      circle.style.animation="ringAnimation 2s linear forwards, twoColorTransition 2s linear forwards";
      resultText.innerHTML =`The code is a mix between self-written and copied.`;
    }else{
      circle.style.animation="ringAnimation 2s linear forwards, threeColorTransition 2s linear forwards";
      resultText.innerHTML =`The code is most probably copied`;
    }
    
}

function showResults() {
  var resultsSection = document.getElementById('resultsSection');
  resultsSection.style.display = 'flex'; // Show the results section
  if (window.innerWidth > 800) {
    let inputSection=document.getElementById('idSection');
    inputSection.style.flex="0 0 60%";}
    else if (window.innerWidth <= 800) {
      let inputSection=document.getElementById('idSection');
      let containerSection=document.getElementById('box');
      inputSection.style.flex="0 0 42.4%";
      containerSection.style.height="800px";}
  
}


function sendTextToBackend(language) {
  
  var text = editor.getValue();
  if (language=='JavaScript'){
    var parsed=parseJavaScriptCode(text);
    console.log('parser', parsed);
    text=parsed;
  }

  // Send the text and selected language to the backend
  fetch('/process', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: text, language: language }),
  })
  .then(response => response.json())
  .then(data => {
      console.log('Response from backend:', data);
      var ratio=parseFloat(data['processed_text']);
      ratioDisplay(ratio);
      console.log(ratio);

      // Handle the response from the backend as needed
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

function checkAndSendText() {
  var language = document.getElementById("selected-item").innerText;

  var text = editor.getValue();
  var errorMessageContainer = document.getElementById('errorMessageContainer');


  if (text.length < 200) {
      showErrorMessage();
  } else {
      errorMessageContainer.style.display = "none";
      // Send the text to backend only if it meets the length requirement
      document.querySelectorAll('#inputButtons button').forEach(button => {button.disabled = true;});
      toggleEditorTyping(false);
      showResults();
      showLoadingSpinner();
      hideResultText();
      hideScoreCircle();
      sendTextToBackend(language);
      
  }
}

function hideErrorMessage() {
  var errorMessageContainer = document.getElementById('errorMessageContainer');
  errorMessageContainer.style.display = "none";
}
function showErrorMessage() {
  var errorMessageContainer = document.getElementById('errorMessageContainer');
  errorMessageContainer.style.display = "flex";
}








function adjustFlexProperty() {
  var resultsSection = document.getElementById('resultsSection');
  var results = window.getComputedStyle(resultsSection);
  var res = results.getPropertyValue('display');

  var inputElement = document.querySelector('.input');
  let containerSection=document.getElementById('box');

      

  // Check if the viewport width is less than 700px and resultsSection is visible
  if (window.innerWidth < 800 && res !== 'none') {
    // Change the flex property of .input to 43%
    inputElement.style.flex = '0 0 42.4%';
    containerSection.style.height="800px";

  } else if (window.innerWidth >= 800 && res !== 'none') {
    // Check if the viewport width is 700px or more and resultsSection is visible
    // Change the flex property of .input back to its original value (60%)
    inputElement.style.flex = '0 0 60%';
    containerSection.style.height="600px";
  }
}

// Call the function initially to set the flex property based on the initial viewport size


// Listen for the resize event on the window object to dynamically adjust the flex property when the window is resized
window.addEventListener('resize', adjustFlexProperty);
// var ratio=0.8;
// ratioDisplay(ratio);

var dropdownBtn=document.querySelector('.dropdown-btn');
var dropdownMenu=document.querySelector('.dropdown-menu');
var items = document.querySelectorAll('.item');
var selectedItem= document.getElementById('selected-item');

// Add global event listener for outside clicks
window.addEventListener('click',function(){
  closeMenu();
});


// Dropdown Btn Event Listener
dropdownBtn.addEventListener('click',(e) =>{
  e.stopPropagation();
  toggleMenu();
});

// Add Click Event Listeners to Each Item
items.forEach((item) => item.addEventListener('click',itemClickHandler))
// Toggle Menu
function toggleMenu(){
  dropdownMenu.classList.toggle('open');
}
// Close Menu
function closeMenu(){
  dropdownMenu.classList.remove('open');
}
// Item Click Handler
function itemClickHandler(e){
  e.stopPropagation();
  selectedItem.innerText=e.target.innerText;
  makechangesdropDownbtn();
  // change active class
  items.forEach((item) => item.classList.remove('active'))
  // add active class to clicked item
  e.target.classList.add('active')
  closeMenu();
}

editor.on('mousedown', function() {
  hideErrorMessage();
});



function makechangesdropDownbtn(){
  if(selectedItem.innerText=='C'){
    dropdownBtn.style.width='25px';
    window.editor.setOption("mode", 'text/x-csrc');
  }else if(selectedItem.innerText=='Python'){
    dropdownBtn.style.width='50px';
    window.editor.setOption("mode", 'python');
  }else if(selectedItem.innerText=='JavaScript'){
    dropdownBtn.style.width='65px';
    CodeMirror.fromTextArea
    window.editor.setOption("mode", 'javascript');
  }

}

