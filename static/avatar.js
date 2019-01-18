var username;

var currentEyes;
var currentNose;
var currentMouth;
var currentColor;

window.onload = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      username = this.responseText;
      updateCurrentValues();
    }
  };
  xhttp.open("GET", "/get_username", true);
  xhttp.send();
};

var updateCurrentValues = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      var response = this.responseText;
      console.log(response);
      var obj = JSON.parse(response);
      currentEyes = obj.eyes;
      currentNose = obj.nose;
      currentMouth = obj.mouth;
      currentColor = obj.color;
      console.log('got current values');
      displayCurrentAvatar();
    }
  };
  xhttp.open("GET", "/get_avatar_json", true);
  xhttp.send();
};

var displayCustomAvatar = function (eyes, nose, mouth, color) {
  url = "https://api.adorable.io/avatars/face/" + eyes + "/" + nose + "/" + mouth + "/" + color;
  document.getElementById('avatarBoi').src = url;
  document.getElementById('avatar').src = url;
  console.log(url);
};

var displayCurrentAvatar = function () {
  displayCustomAvatar(currentEyes, currentNose, currentMouth, currentColor);
};

var updateEyes = function (newVal) {
  displayCustomAvatar(newVal, currentNose, currentMouth, currentColor);
};

var updateNose = function (newVal) {
  displayCustomAvatar(currentEyes, newVal, currentMouth, currentColor);
};

var updateMouth = function (newVal) {
  displayCustomAvatar(currentEyes, currentNose, newVal, currentColor);
};

var updateColor = function (newVal) {
  displayCustomAvatar(currentEyes, currentNose, currentMouth, newVal);
};

var changeEyes = function (newVal) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      displayCurrentAvatar();
      updateCurrentValues();
    }
  };
  xhttp.open("GET", "/update_avatar?what=eyes&newVal=" + newVal, true);
  xhttp.send();
};

var changeNose = function (newVal) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      displayCurrentAvatar();
      updateCurrentValues();
    }
  };
  xhttp.open("GET", "/update_avatar?what=noses&newVal=" + newVal, true);
  xhttp.send();
};

var changeMouth = function (newVal) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      displayCurrentAvatar();
      updateCurrentValues();
    }
  };
  xhttp.open("GET", "/update_avatar?what=mouths&newVal=" + newVal, true);
  xhttp.send();
};

var changeColor = function (newVal) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      displayCurrentAvatar();
      updateCurrentValues();
    }
  };
  xhttp.open("GET", "/update_avatar?what=color&newVal=" + newVal, true);
  xhttp.send();
};

var confirmPurchase = function (cash, feature, newVal, price) {
  /*
  if (cash < price) {
    alert(`You cannot afford ${newVal}! It costs ${price} BigCoins!`);
  }
  else (confirm(`${newVal.italics()} costs ${price}. Are you sure you want to purchase ${newVal.italics()}?`)) {
    purchaseFeature(feature, newVal);
  }*/
  console.log(cash, feature, newVal, price);
  if (cash < price) {
    window.alert(`You cannot afford ${newVal}! It costs ${price} BigCoins!`);
  } else if (confirm(`${newVal} costs ${price}.\nAre you sure you want to purchase ${newVal}?`)) {
    var newPrice = cash - price;
    purchaseFeature(feature, newVal, newPrice);
  }
};

var updateFeature = function (newVal, newPrice) {
  console.log(newVal);
  if (document.getElementById(newVal).innerHTML == 'PURCHASE') {
    document.getElementById(newVal).innerHTML = 'OWNED';
  } else {
    document.getElementById(newVal).className = "btn btn-success ml-1 mb-2";
  }
  document.getElementById('bigcoins').innerHTML = newPrice
  window.location.reload()

}

var purchaseFeature = function (feature, newVal, newPrice) {
  console.log(feature, newVal);
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      updateFeature(newVal, newPrice);
    }
  }
  xhttp.open("GET", `/purchase?feature=${feature}&value=${newVal}`, true);
  xhttp.send();
};
