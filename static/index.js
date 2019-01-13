// load login and register menu

window.onload = function () {
    toLogin();
};

// display register form
var toRegister = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('loginRegister').innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/get_snippet?snippet=register", true);
    xhttp.send();
};

// display login form
var toLogin = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('loginRegister').innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/get_snippet?snippet=login", true);
    xhttp.send();
};
