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
            document.getElementById('firstNameButton').innerHTML = '<button type="button" class="btn rounded btn-warning btn-block" onclick="displayFirstNameForm();">Update First Name</button>';
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
            document.getElementById('lastNameButton').innerHTML = '<button type="button" class="btn rounded btn-warning btn-block" onclick="displayLastNameForm();">Update Last Name</button>';
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
            document.getElementById('emailButton').innerHTML = '<button type="button" class="btn rounded btn-warning btn-block" onclick="displayEmailForm();">Update Email</button>';
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
            document.getElementById('phoneButton').innerHTML = '<button type="button" class="btn rounded btn-warning btn-block" onclick="displayPhoneForm();">Update Phone Number</button>';
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
            document.getElementById('bioButton').innerHTML = '<button type="button" class="rounded btn btn-warning" onclick="displayBioForm();">Update Biography</button>';
        }
    };
    xhttp.open("GET", "/get_info?val=bio&username=" + username, true);
    xhttp.send();

};

var displayFirstNameForm = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var obj = JSON.parse(this.responseText);
            document.getElementById('firstName').innerHTML = obj.input;
            document.getElementById('firstNameButton').innerHTML = obj.buttons;
        }
    };
    xhttp.open("GET", "/get_profile_button?val=FirstName&username=" + username, true);
    xhttp.send();
};

var displayLastNameForm = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var obj = JSON.parse(this.responseText);
            document.getElementById('lastName').innerHTML = obj.input;
            document.getElementById('lastNameButton').innerHTML = obj.buttons;
        }
    };
    xhttp.open("GET", "/get_profile_button?val=LastName&username=" + username, true);
    xhttp.send();
};

var displayEmailForm = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var obj = JSON.parse(this.responseText);
            document.getElementById('email').innerHTML = obj.input;
            document.getElementById('emailButton').innerHTML = obj.buttons;
        }
    };
    xhttp.open("GET", "/get_profile_button?val=Email&username=" + username, true);
    xhttp.send();
};

var displayPhoneForm = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var obj = JSON.parse(this.responseText);
            document.getElementById('phone').innerHTML = obj.input;
            document.getElementById('phoneButton').innerHTML = obj.buttons;
        }
    };
    xhttp.open("GET", "/get_profile_button?val=Phone&username=" + username, true);
    xhttp.send();
};

var displayBioForm = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var obj = JSON.parse(this.responseText);
            document.getElementById('bio').innerHTML = obj.input;
            document.getElementById('bioButton').innerHTML = obj.buttons;
        }
    };
    xhttp.open("GET", "/get_profile_button?val=Bio&username=" + username, true);
    xhttp.send();
};

var updateFirstName = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            displayFirstName();
        }
    };
    var newText = document.getElementById('FirstName').value;
    xhttp.open("GET", "/update_info?what=first&newVal=" + newText + "&username=" + username, true);
    xhttp.send();
};

var updateLastName = function () {

};

var updateEmail = function () {

};

var updatePhone = function () {

};

var updateBio = function () {

};
