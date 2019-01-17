var sidebarOut = true;
var pid;

var setup = function () {
  displayAvatar();
  pid = document.getElementById('toClipboard').value;
  displayDash();
};

var setPID = function () {
  pid = document.getElementById('toClipboard').value;
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
      setMinDate();
    }
  };
  xhttp.open("GET", `/get_dashboard?pid=${pid}`, true);
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
  };
  xhttp.open("GET", `/get_snippet?snippet=tasks&pid=${pid}`, true);
  xhttp.send();
};


var displayAddTask = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById('form_content').innerHTML = this.responseText;
      setMinDate();
    }
  };
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
  };
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
  };
  xhttp.open("GET", `/get_snippet?snippet=privateInbox&pid=${pid}`, true);
  xhttp.send();
};

var getUserImage = function (msgID, user) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById(msgID).src = this.responseText;
    }
  };
  xhttp.open("GET", `/get_avatar_from_get?username=${user}`, true);
  xhttp.send();
};

var deleteMessage = function (msgID) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      displayPrivateInbox();
    }
  };
  xhttp.open("GET", `/delete_private_msg?msgID=` + msgID, true);
  xhttp.send();
};

var submitNewTask = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      displayTasks();
    }
  };
  var task = document.getElementById('newTaskName').value;
  var desc = document.getElementById('newTaskDescription').value;
  var prio = document.getElementById('priority').value;
  var date = document.getElementById('date').value;
  console.log(task);
  console.log(desc);
  console.log(prio);
  console.log(date);

  xhttp.open("GET", "/new_task?task=" + task + "&description=" + desc + "&priority=" + prio + "&due_date=" + date + "&status=" + "0&pid=" + pid, true);
  xhttp.send();
};

// msg fxns

var submitTeamMsg = function () {
  var msg = encodeURIComponent(document.getElementById('msg').value);
  if (msg == "") {
    console.log("not sending because blank message!");
    return;
  }
  currentDate = new Date();
  year = currentDate.getFullYear();
  month = currentDate.getMonth() + 1;
  day = currentDate.getDate();
  hour = currentDate.getHours();
  minute = currentDate.getMinutes();
  var time = `${year}/${month}/${day} - ${hour}:${minute}`;
  console.log(msg);
  console.log(time);

  var url = `/new_tmsg?msg=${msg}&pid=${pid}&timestamp=${time}`;
  console.log("URL BEFORE URL\n" + url)

  url = encodeURI(url);
  console.log("URL AFTER URL\n" + url)


  // xhttp
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      displayTeamInbox();
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
};

var submitPrivateMsg = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      displayPrivateInbox();
    }
  };
  var msg_to = document.getElementById('selectTo').value;
  var msg = encodeURIComponent(document.getElementById('msg').value);
  currentDate = new Date();
  year = currentDate.getFullYear();
  month = currentDate.getMonth() + 1;
  day = currentDate.getDate();
  hour = currentDate.getHours();
  minute = currentDate.getMinutes();
  var time = `${year}/${month}/${day} - ${hour}:${minute}`;
  console.log(msg_to);
  console.log(msg);
  console.log(time);
  xhttp.open("GET", `/new_private_message?address=${msg_to}&msg=${msg}&pid=${pid}&timestamp=${time}`, true);
  xhttp.send();
};

var updateMsgs = function () {

};


var displayIpsum = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById('contentColumn').innerHTML = this.responseText;

    }
  };
  xhttp.open("GET", "/get_snippet?snippet=ipsum", true);
  xhttp.send();
};



var getData = function () {
  var wc = document.getElementById('wordCount').value;
  var sc = document.getElementById('sentenceCount').value;
  var type = document.querySelector('input[name="format"]:checked').value;

  console.log("WC: " + wc + "\nSC: " + sc + "\ntype: " + type);

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState = 4 && this.status == 200) {
      console.log('Got response');
      var d = document.getElementById('data');
      d.value = this.responseText;
      d.hidden = false;
    }
  };
  xhttp.open("GET", "/get_data?sentenceCount=" + sc + "&wordCount=" + wc + "&format=" + type, true);
  xhttp.send();
};





// update char counts

var updateNewTaskCharCount = function () {
  var name = document.getElementById('newTaskName').value;
  var length = name.length;
  document.getElementById('newTaskCharCount').innerHTML = length + "/50";
};
var updateNewDescriptionCharCount = function () {
  var name = document.getElementById('newTaskDescription').value;
  var length = name.length;
  document.getElementById('newTaskDescriptionCount').innerHTML = length + "/150";
};
var updateMsgCharCount = function () {
  var name = document.getElementById('msg').value;
  var length = name.length;
  document.getElementById('msgCharCount').innerHTML = length + "/140";
};

var setMinDate = function () {
  n = new Date();
  y = n.getFullYear();
  m = n.getMonth() + 1;
  d = n.getDate();
  date = y + "/" + m + "/" + d;
  document.getElementById('date').min = date;
  console.log(date);
};

var setID = function () {
  id = document.getElementById('toClipboard').innerHTML
  document.getElementById('task_form').action = "/new_task/" + id
};

var resetTextarea = function (v) {
  document.getElementById('toClipboard').value = v;
};

var moveTo = function (what, where) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      displayTasks();
    }
  };
  xhttp.open("GET", "/move_task?what=" + what + "&where=" + where, true);
  xhttp.send();
};









//
