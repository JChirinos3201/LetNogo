window.onload = function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('loginRegister').innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/get_snippet?snippet=login", true);
    xhttp.send();
};
