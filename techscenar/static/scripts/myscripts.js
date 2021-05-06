var coll = document.getElementsByClassName("events-vert");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

function startTime() {
    var today, r, t, li, a, b, ul;
    today = new Date();
    t = today.getTime();
    ul = document.getElementById("myUL");
    li = ul.getElementsByClassName('event_li');

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByClassName("begin_epoch")[0].innerText;
        b = li[i].getElementsByClassName("end_epoch")[0].innerText;
        if (b > t && t > a) {
            li[i].style.backgroundColor = "lightblue";
        } else {
            li[i].style.backgroundColor = "";
        }
    }
    r = setTimeout(startTime, 10000);

}

function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByClassName('event_li');

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByClassName("searchstring")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function myFunction2() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByClassName('date_li');

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByClassName("searchstring_date")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}