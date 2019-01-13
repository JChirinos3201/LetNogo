var username;

window.onload = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            username = this.responseText;
            displayFirstName();
            displayLastName();
            displayEmail();
            displayPhone();
            displayBio();
        }
    };
    xhttp.open("GET", "/get_username", true);
    xhttp.send();
};

var displayFirstName = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById('firstName').innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?val=first&username=" + username, true);
    xhttp.send();
};

var displayLastName = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById('lastName').innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?val=last&username=" + username, true);
    xhttp.send();
};

var displayEmail = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById('email').innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?val=email&username=" + username, true);
    xhttp.send();

};

var displayPhone = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById('phone').innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?val=phone&username=" + username, true);
    xhttp.send();

};

var displayBio = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById('bio').innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?val=bio&username=" + username, true);
    xhttp.send();

};

var displayFirstNameForm = function () {


};

var displayLastNameForm = function () {

};

var displayEmailForm = function () {

};

var displayPhoneForm = function () {

};

var displayBioForm = function () {

};
