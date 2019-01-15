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
    };
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
    };
    xhttp.open("GET", "/get_snippet?snippet=login", true);
    xhttp.send();
};

var firstValid = false;
var lastValid = false;
var emailValid = false;
var userValid = false;
var passValid = false;
var passCheckValid = false;

var phoneValid = true; // can be blank, so true by default

var toggleSubmit = function () {
    if (firstValid && lastValid && emailValid && phoneValid && userValid && passValid && passCheckValid) {
        document.getElementById('register').disabled = false;
        console.log('submit button active');
    } else {
        document.getElementById('register').disabled = true;
        console.log('submit button disabled');
    }
};

var updateError = function () {
    var err = document.getElementById('err');
    if (!firstValid) {
        if (document.getElementById('first').value == "") {
            err.innerHTML = "Invalid first name!";
        } else {
            err.innerHTML = "Invalid first name! Please omit \"?\", \"#\", and unnecessary whitespace";
        }
        err.style.display = "block";
    } else if (!lastValid) {
        if (document.getElementById('last').value == "") {
            err.innerHTML = "Invalid last name!";
        } else {
            err.innerHTML = "Invalid last name! Please omit \"?\", \"#\", and unnecessary whitespace";
        }
        err.style.display = "block";
    } else if (!emailValid) {
        err.innerHTML = "Invalid email address!";
        err.style.display = "block";
    } else if (!phoneValid) {
        err.innerHTML = "Invalid phone number!";
        err.style.display = "block";
    } else if (document.getElementById('username').value == "") {
        err.innerHTML = "Invalid username!";
        err.style.display = "block";
    } else if (!userValid) {
        err.innerHTML = "Username taken!";
        err.style.display = "block";
    } else if (!passValid) {
        err.innerHTML = "Invalid password!";
        err.style.display = "block";
    } else if (!passCheckValid) {
        err.innerHTML = "Passwords don't match!";
        err.style.display = "block";
    } else {
        err.innerHTML = "";
        err.style.display = "none";
    }
};

var checkFirst = function () {
    var first = document.getElementById('first').value;
    var re = /[?#]/;
    if (re.test(first) || first.trim() != first) {
        firstValid = false;
    } else {
        firstValid = true;
    }
    updateError();
    toggleSubmit();
};

var checkLast = function () {
    var last = document.getElementById('last').value;
    var re = /[?#]/;
    if (re.test(last) || last.trim() != last) {
        lastValid = false;
    } else {
        lastValid = true;
    }
    updateError();
    toggleSubmit();
};

var checkEmail = function () {
    var email = document.getElementById('email').value;
    // regex from https://emailregex.com/
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (re.test(email) && email.trim() == email) {
        emailValid = true;
    } else {
        emailValid = false;
    }
    updateError();
    toggleSubmit();
};

var checkPhone = function () {
    var phone = document.getElementById('phone').value;
    if (phone == "") {
        phoneValid = true;
    } else {
        var re = /^\(?[2-9]{3}\)?(\-|\ )?[0-9]{3}(\-|\ )?[0-9]{4}$/;
        if (re.test(phone) && phone.trim() == phone) {
            phoneValid = true;
        } else {
            phoneValid = false;
        }
    }
    updateError();
    toggleSubmit();
};

var checkUser = function () {
    var user = document.getElementById('username').value;
    if (user == "") {
        userValid = false;
        updateError();
        toggleSubmit();
        return;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = this.responseText;
            if (response == 'good') {
                userValid = true;
            } else {
                userValid = false;
            }
            updateError();
            toggleSubmit();
        }
    };
    xhttp.open("GET", "/check_user?user=" + user, true);
    xhttp.send();
};

var checkPass = function () {
    var pat = /^[a-z0-9.]{8,}/i;
    var pass = document.getElementById('password').value;
    if (pat.test(pass)) {
        passValid = true;
    } else {
        passValid = false;
    }
    updateError();
    toggleSubmit();
};

var checkEquality = function () {
    var pass = document.getElementById('password').value;
    var passCheck = document.getElementById('passwordVerify').value;
    console.log(pass);
    console.log(passCheck);

    if (pass == passCheck) {
        passCheckValid = true;
    } else {
        passCheckValid = false;
    }
    updateError();
    toggleSubmit();
};
