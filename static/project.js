var sidebarOut = true;
var pid;

window.onload = function () {
    displayAvatar();
    displayDash();
    pid = document.getElementById('project_id');
};

var toggleSidebar = function () {
    var sb = document.getElementById('buttons');
    if (sidebarOut) {
        var op = 1;
        var timer = setInterval(function () {
            if (op <= 0.1) {
                clearInterval(timer);
                sb.style.display = "none";
            }
            sb.style.opacity = op;
            sb.style.filter = 'alpha)opacity=' + op * 100 + ")";
            op -= op * 0.1;
        }, 10);
        sidebarOut = false;
    } else {
        var op = 0.1;
        sb.style.display = "block";
        var timer = setInterval(function () {
            if (op >= 0.9) {
                clearInterval(timer);
            }
            sb.style.opacity = op;
            sb.style.filter = 'alpha)opacity=' + op * 100 + ")";
            op += op * 0.1;
        }, 10);
        sidebarOut = true;
    }
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

var copyToClipboard = function () {
    var copyText = document.getElementById('toClipboard');
    copyText.select();
    document.execCommand('copy');
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
    xhttp.open("GET", `/get_snippet?snippet=tasks&pid=${pid}`, true);
    xhttp.send();
};


var displayAddTask = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('form_content').innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/get_snippet?snippet=newTask", true);
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
    xhttp.open("GET", `/get_snippet?snippet=teamInbox&pid=${pid}`, true);
    xhttp.send();
};

// private inbox
var displayPrivateInbox = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;

        }
    }
    xhttp.open("GET", `/get_snippet?snippet=privateInbox&pid=${pid}`, true);
    xhttp.send();
};

var getUserImage = function (msgID, user) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById(msgID).src = this.responseText;
        }
    }
    xhttp.open("GET", `/get_avatar_from_get?username=` + user, true);
    xhttp.send();
};

var deleteMessage = function (msgID) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            displayPrivateInbox();
        }
    }
    xhttp.open("GET", `/delete_private_msg?msgID=` + msgID, true);
    xhttp.send();
};

// update char counts

var updateNewTaskCharCount = function () {
    var name = document.getElementById('newTaskName').value;
    var length = name.length;
    document.getElementById('newTaskCharCount').innerHTML = length + "/100";
};
var updateNewDescriptionCharCount = function () {
    var name = document.getElementById('newTaskDescription').value;
    var length = name.length;
    document.getElementById('newTaskDescriptionCount').innerHTML = length + "/150";
};

var setMinDate = function() {
    n = new Date();
    y = n.getFullYear();
    m = n.getMonth() + 1;
    d = n.getDate();
    date =  y + "/" + m + "/" + d;
    document.getElementById('date').min = date;
    console.log(date);
};

var setID = function() {
    id = document.getElementById('toClipboard').innerHTML
    document.getElementById('task_form').action = "/new_task/" + id
};
