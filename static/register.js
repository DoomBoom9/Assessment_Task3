let i=0;
const inputs = document.querySelectorAll("input");
const form = document.getElementById("form");
const submit = document.getElementById("submit");
const username = document.getElementById('username')
const password = document.getElementById('password')
const phoneNumber = document.getElementById('phoneNumber')
const address = document.getElementById('address')
const securityA1 = document.getElementById('securityA1')
const securityA2 = document.getElementById('securityA2')
const securityA3 = document.getElementById('securityA3')
const file = document.getElementById('file')

//sanitises input
function sanitise(input){
  const map = {
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    "/": '&#x2F;',
  };
  const reg = /[&<>"'/]/ig;
  return input.replace(reg, (match)=>(map[match]));  
}

//checks if file has the correct extension and file size
function validateFile(){
  var fileInput = document.getElementById('file');
  var filePath = fileInput.value;
  var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

  if (fileInput.files.length > 1){
    //alert for too many files error
    return false
  } if (!allowedExtensions.exec(filePath)){
    //alert for filetype error
    fileInput.value='';
    return false
  } if(fileInput.files.length == 1) {
      var fsize = fileInput.files.item(0).size;
      fsize = Math.round((fsize/1024));

      if (fsize > 2048){
        //alert for filesize error
        return false
      }
  } else {
    //alert file valid
    return true
  }
}
//validates phone Number
function validatePhoneNumber(input){
  if(
    input.length == 10 &&
    /\d/.test(input)
  ){
    return true;
  } else {
    return false;
  }
}

//validates username
function validateUsername(input){
  if(
    input.length <= 25 
  ){
    return true;
  } else {
    return false;
  }
}

//validates pword
function validatePassword(input){
  if (
    input.length >= 12 &&
    input.length <= 25 &&
    /[a-z]/.test(input) &&
    /[A-Z]/.test(input) &&
    /\d/.test(input) &&
    /[#.?!@$%^&*-]/.test(input)
  ) {
    return true;
  } else {
    return false;
  }
}

//validates other fields
function validateDefault(input){
  if(input.length < 50){
    return true
  } else {
    return false
  }
}

document.addEventListener('DOMContentLoaded', function() {
  //safe admin action
  //changes colour of element when a button is clicked
  document.getElementById('adminButton').addEventListener('click', function() {
    let heading = document.getElementById("adminAction");
    let colours = ["orange","yellow","lightgreen","green","olive","lightblue","blue", "lightpurple","purple", "pink","red"];
    if(i>11){
      i=0
    }
    heading.style.color = colours[i];
    i++;
  });
});

//handles validation and sanitisation on submit
form.addEventListener('submit', function(event){

  //pre emptively invalidates user input if honeypot is triggered
  if(document.getElementById('honeypot').value != ""){
    event.preventDefault();
    return false;
  }

  let isValid;
  for (let count = 0; count<inputs.length; count++){ //iterates through inputs
    if (inputs[count].id == 'password'){
      isValid = validatePassword(inputs[count].value); //checks if password is valid
      if(isValid == false){
        
        event.preventDefault();
        return false;
      }
    } else if (inputs[count].id == 'username'){
      isValid = validateUsername(inputs[count].value); //checks if username is valid
      if (isValid == false){
        
        event.preventDefault();
        return false;
      }
    } else if (inputs[count].id == 'phoneNumber'){
      isValid = validatePhoneNumber(inputs[count].value); //checks if phonenumber is valid
      if (isValid == false){
        
        event.preventDefault();
        return false;
      }
    } else if(inputs[count].id == 'file'){
      isValid = validateFile();//if this shits itself pass in inputs[count].value, checks if file is valid
      if (isValid == false){
        
        event.preventDefault();
        return false;
      }
    } else if(inputs[count].id != 'token'){ //checks 'defaults' (longer inputs eg. address that aren't the CSRF token) are valid
      isValid = validateDefault(inputs[count].value);
      if (isValid == false){
        
        event.preventDefault();
        return false;
      }
    }
    inputs[count].value = sanitise(inputs[count].value); //makes input websafe through sanitisation
  }

  //submits form if form is valid
  if (isValid == True){
    
    event.preventDefault();
    
    return true;
  }
});

username.addEventListener('keyup', function(){
  if (username.value.length <= 25){
    document.getElementById('usernameLengthReq').hidden = true;
  } else {
    document.getElementById('usernameLengthReq').hidden = false;
  }
});

//hide or display Password Reqs on Blur
password.addEventListener('keyup', function(){

  //length
  if ((password.value.length < 11) || (password.value.length > 25)){
    document.getElementById('passwordLengthReq').hidden = false;
  } else {
    document.getElementById('passwordLengthReq').hidden = true;
  }

  //Uppercase
  if (/[A-Z]/.test(password.value) == true){
    document.getElementById('passwordUpperReq').hidden = true;
  } else {
    document.getElementById('passwordUpperReq').hidden = false;
  }

  //lowercase
  if (/[a-z]/.test(password.value) == true){
    document.getElementById('passwordLowerReq').hidden = true;
  } else {
    document.getElementById('passwordLowerReq').hidden = false;
  }

  //digits/integers
  if (/\d/.test(password.value) == true){
    document.getElementById('passwordIntReq').hidden = true;
  } else {
    document.getElementById('passwordIntReq').hidden = false;
  }

  //special characters
  if (/[#.?!@$%^&*-]/.test(password.value) == true){
    document.getElementById('passwordSpecialReq').hidden = true;
  } else {
    document.getElementById('passwordSpecialReq').hidden = false;
  }
});

phoneNumber.addEventListener('keyup', function(){
  if (phoneNumber.value.length != 10){
    document.getElementById('phoneLengthReq').hidden = false;
  } else {
    document.getElementById('phoneLengthReq').hidden = true;
  }

  if (/\d/.test(phoneNumber.value) == true){
    document.getElementById('phoneTypeReq').hidden = true;
  } else {
    document.getElementById('phoneTypeReq').hidden = false;
  }
});

address.addEventListener('keyup', function(){
  if (address.value.length > 50){
    document.getElementById('addressLengthReq').hidden = false;
  } else {
    document.getElementById('addressLengthReq').hidden = true;
  }
});

securityA1.addEventListener('keyup', function(){
  if (securityA1.value.length > 50){
    document.getElementById('securityA1LengthReq').hidden = false;
  } else {
    document.getElementById('securityA1LengthReq').hidden = true;
  }
});

securityA2.addEventListener('keyup', function(){
  if (securityA2.value.length > 50){
    document.getElementById('securityA2LengthReq').hidden = false;
  } else {
    document.getElementById('securityA2LengthReq').hidden = true;
  }
});

securityA3.addEventListener('keyup', function(){
  if (securityA3.value.length > 50){
    document.getElementById('securityA3LengthReq').hidden = false;
  } else {
    document.getElementById('securityA3LengthReq').hidden = true;
  }
});

file.addEventListener('change', function(){
  var filePath = file.value;
  var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
  if (!allowedExtensions.exec(filePath) && (file.files.length == 1)){
    document.getElementById('fileTypeReq').hidden = false;
  } if(file.files.length == 1) {
    var fsize = file.files.item(0).size;
    fsize = Math.round((fsize/1024));

    if (fsize > 2048){
      //alert for filesize error
      document.getElementById('fileSizeReq').hidden = false;
    }
  } else {
    document.getElementById('fileTypeReq').hidden = true;
    document.getElementById('fileSizeReq').hidden = true;
  }




});