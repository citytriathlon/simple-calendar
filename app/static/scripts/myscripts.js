var hasScrolledInitially = false;

function normalizeString(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toUpperCase();
}

function filterEvents() {
  var input, filter, ul, dateLiElements, eventLiElements, dayMatch;
  input = document.getElementById("myInput");
  filter = normalizeString(input.value);
  ul = document.getElementById("myUL");
  dateLiElements = ul.getElementsByClassName("date_li");

  for (var i = 0; i < dateLiElements.length; i++) {
    eventLiElements = dateLiElements[i].getElementsByClassName("event_li");
    dayMatch = false;

    for (var j = 0; j < eventLiElements.length; j++) {
      var eventString =
        eventLiElements[j].getElementsByClassName("searchstring")[0]
          .textContent;
      var eventDateString =
        eventLiElements[j].getElementsByClassName("searchstring_date")[0]
          .textContent;

      if (
        normalizeString(eventString).includes(filter) ||
        normalizeString(eventDateString).includes(filter)
      ) {
        eventLiElements[j].style.display = "";
        dayMatch = true;
      } else {
        eventLiElements[j].style.display = "none";
      }
    }

    dateLiElements[i].style.display = dayMatch ? "" : "none";
  }
}

document.getElementById("myInput").onkeyup = filterEvents;

function startTime() {
  var today, r, t, li, a, b, ul;
  today = new Date();
  t = today.getTime();
  ul = document.getElementById("myUL");
  li = ul.getElementsByClassName("event_li");

  for (var i = 0; i < li.length; i++) {
    a = parseInt(li[i].getElementsByClassName("begin_epoch")[0].innerText);
    b = parseInt(li[i].getElementsByClassName("end_epoch")[0].innerText);

    if (b > t && t > a) {
      li[i].style.backgroundColor = "lightblue";
    } else {
      li[i].style.backgroundColor = t > b ? "lightgray" : "";
    }
  }

  setTimeout(startTime, 10000);
}

function initialScrollToEvent() {
  if (hasScrolledInitially) return;

  var today, t, li, a, b, ul, currentEventFound = false, nextEventElement = null;
  today = new Date();
  t = today.getTime();
  ul = document.getElementById("myUL");
  li = ul.getElementsByClassName("event_li");

  for (var i = 0; i < li.length; i++) {
    a = parseInt(li[i].getElementsByClassName("begin_epoch")[0].innerText);
    b = parseInt(li[i].getElementsByClassName("end_epoch")[0].innerText);

    if (b > t && t > a && !currentEventFound) {
      li[i].scrollIntoView({ behavior: "smooth", block: "center" });
      currentEventFound = true;
    } else if (a > t && !nextEventElement) {
      nextEventElement = li[i];
    }
  }

  if (!currentEventFound && nextEventElement) {
    nextEventElement.scrollIntoView({ behavior: "smooth", block: "center" });
    hasScrolledInitially = true;
  }
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
  initialScrollToEvent();
});