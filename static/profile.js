var username;

window.onload = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            username = this.responseText;
        }
    };
    xhttp.open("GET", "/get_username", true);
    xhttp.send();
};

var displayFirstName = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            username = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?req=first", true);
    xhttp.send();
};

var displayLastName = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            username = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?req=last", true);
    xhttp.send();
};

var displayEmail = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            username = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?req=email", true);
    xhttp.send();

};

var displayPhone = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            username = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?req=phone", true);
    xhttp.send();

};

var displayBio = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            username = this.responseText;
        }
    };
    xhttp.open("GET", "/get_info?req=bio", true);
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
