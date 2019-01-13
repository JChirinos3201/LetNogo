// avatar

var originalAvatar = document.getElementById("avatar").src;

window.onload = function () {
    var originalAvatar = document.getElementById("avatar").src;
    console.log(originalAvatar);
};

// eye fxns

var changeEye = function(e) {
  var eye = this.innerHTML
  var originalEye = originalAvatar.indexOf('eye');
  var newEye = originalAvatar.replace(originalAvatar.slice(originalEye, originalEye + 5), eye);
  document.getElementById("avatar").src = newEye;
}


var eyeList = document.getElementById("eye_list").getElementsByTagName('li')

for (var i = 0; i < eyeList.length; i++) {
  eyeList[i].addEventListener('mouseover', changeEye);
  eyeList[i].addEventListener('mouseout', function(e){
      document.getElementById("avatar").src = originalAvatar;
  });
}

// nose fxns
var changeNose = function(e) {
  var nose = this.innerHTML
  var originalNose = originalAvatar.indexOf('nose');
  var newNose = originalAvatar.replace(originalAvatar.slice(originalNose, originalNose + 5), nose);
  document.getElementById("avatar").src = newNose;
}

var noseList = document.getElementById("nose_list").getElementsByTagName('li')

for (var i = 0; i < noseList.length; i++) {
  noseList[i].addEventListener('mouseover', changeNose);
  noseList[i].addEventListener('mouseout', function(e){
      document.getElementById("avatar").src = originalAvatar;
  });
}


// mouth fxns
var changeMouth = function(e) {
  var mouth = this.innerHTML
  var originalMouth = originalAvatar.indexOf('mouth');
  var newMouth = originalAvatar.replace(originalAvatar.slice(originalMouth, originalMouth + 6), mouth);
  console.log(newMouth)
  document.getElementById("avatar").src = newMouth;
}

var mouthList = document.getElementById("mouth_list").getElementsByTagName('li')

for (var i = 0; i < mouthList.length; i++) {
  mouthList[i].addEventListener('mouseover', changeMouth);
  mouthList[i].addEventListener('mouseout', function(e){
      document.getElementById("avatar").src = originalAvatar;
  });
}
// color fxns?
