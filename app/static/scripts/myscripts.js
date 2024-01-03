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
    var today, r, t, li, a, b, ul, currentEventFound = false, nextEventElement = null;
    today = new Date();
    t = today.getTime();
    ul = document.getElementById("myUL");
    li = ul.getElementsByClassName('event_li');

    for (var i = 0; i < li.length; i++) {
        a = parseInt(li[i].getElementsByClassName("begin_epoch")[0].innerText);
        b = parseInt(li[i].getElementsByClassName("end_epoch")[0].innerText);

        if (b > t && t > a) {
            li[i].style.backgroundColor = "lightblue";
            if (!currentEventFound) {
                li[i].scrollIntoView({ behavior: 'smooth', block: 'center' });
                currentEventFound = true;
            }
        } else {
            li[i].style.backgroundColor = (t > b) ? "lightgray" : "";
            
            if (a > t && !nextEventElement) {
                nextEventElement = li[i];
            }
        }
    }

    if (!currentEventFound && nextEventElement) {
        nextEventElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    r = setTimeout(startTime, 10000);
}



function filterEvents() {
    var input, filter, ul, li, searchStrings, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName('li');

    for (var i = 0; i < li.length; i++) {
        // Combine search strings from both 'searchstring' and 'searchstring_date'
        searchStrings = li[i].getElementsByClassName("searchstring")[0].textContent.toUpperCase() + 
                        li[i].getElementsByClassName("searchstring_date")[0].textContent.toUpperCase();

        if (searchStrings.indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

// Adjust the event listener for the input box
document.getElementById('myInput').onkeyup = filterEvents;

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

