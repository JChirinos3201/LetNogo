window.onload = function () {
    displayExistingProjects();
    displayAvatar();
};

// display avatar

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

// create project

var displayNewProject = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/get_snippet?snippet=newProject", true);
    xhttp.send();
};

// join project

var displayJoinProject = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/get_snippet?snippet=joinProject", true);
    xhttp.send();
};

// existing projects

var displayExistingProjects = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('contentColumn').innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/get_snippet?snippet=projectList", true);
    xhttp.send();
};

// update char counts

var updateNewProjectCharCount = function () {
    var name = document.getElementById('newProjectName').value;
    var length = name.length;
    document.getElementById('newProjectCharCount').innerHTML = length + "/30";
};
