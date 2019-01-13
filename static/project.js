var pid;
window.onload = function () {
    displayAvatar();
    displayTasks();
    pid = document.getElementById('project_id')
};



var displayAvatar = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('avatar').src = this.responseText;
        }
    }
    xhttp.open("GET", "/get_avatar", true);
    xhttp.send();
};


// dashboard
var displayDash = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;
            // console.log(this.responseText);

        }
    }
    xhttp.open("GET", `/get_snippet?snippet=dashboard&pid=${pid}`, true);
    xhttp.send();
};

// tasks
var displayTasks = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;
            // console.log(this.responseText);

        }
    }
    xhttp.open("GET", `/get_snippet?snippet=tasks&pid=${pid}"`, true);
    xhttp.send();
};

// team inbox
var displayTeamInbox = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;
            // console.log(this.responseText);

        }
    }
    xhttp.open("GET", `/get_snippet?snippet=teamInbox&pid=${pid}`", true);
    xhttp.send();
};

// private inbox
var displayPrivateInbox = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;
            // console.log(this.responseText);

        }
    }
    xhttp.open("GET", `/get_snippet?snippet=privateInbox&pid=${pid}`, true);
    xhttp.send();
};
