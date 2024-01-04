function normalizeString(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toUpperCase();
}

function filterEvents() {
  var input, filter, ul, dateLi, eventLi, decodedSearchString;
  input = document.getElementById("myInput");
  filter = normalizeString(input.value);
  ul = document.getElementById("myUL");
  dateLi = ul.getElementsByClassName("date_li");

  for (var i = 0; i < dateLi.length; i++) {
    eventLi = dateLi[i].getElementsByClassName("event_li");

    for (var j = 0; j < eventLi.length; j++) {
      var searchStringElement =
        eventLi[j].getElementsByClassName("searchstring")[0];

      decodedSearchString = normalizeString(
        htmlDecode(searchStringElement.textContent)
      );

      if (decodedSearchString.includes(filter)) {
        eventLi[j].style.display = "";
      } else {
        eventLi[j].style.display = "none";
      }
    }
  }
}

document.getElementById("myInput").onkeyup = filterEvents;

function startTime() {
  var today,
    r,
    t,
    li,
    a,
    b,
    ul,
    currentEventFound = false,
    nextEventElement = null;
  today = new Date();
  t = today.getTime();
  ul = document.getElementById("myUL");
  li = ul.getElementsByClassName("event_li");

  for (var i = 0; i < li.length; i++) {
    a = parseInt(li[i].getElementsByClassName("begin_epoch")[0].innerText);
    b = parseInt(li[i].getElementsByClassName("end_epoch")[0].innerText);

    if (b > t && t > a) {
      li[i].style.backgroundColor = "lightblue";
      if (!currentEventFound) {
        li[i].scrollIntoView({ behavior: "smooth", block: "center" });
        currentEventFound = true;
      }
    } else {
      li[i].style.backgroundColor = t > b ? "lightgray" : "";
      if (a > t && !nextEventElement) {
        nextEventElement = li[i];
      }
    }
  }

  if (!currentEventFound && nextEventElement) {
    nextEventElement.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  setTimeout(startTime, 10000);
}

var coll = document.getElementsByClassName("events-vert");
for (var i = 0; i < coll.length; i++) {
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

document.addEventListener("DOMContentLoaded", function () {
  startTime();
});
