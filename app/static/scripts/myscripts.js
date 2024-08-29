var hasScrolledInitially = false;

function normalizeString(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toUpperCase();
}

function filterEvents() {
  var input = document.getElementById("myInput");
  var filter = normalizeString(input.value);
  var ul = document.getElementById("myUL");
  var dateLiElements = ul.getElementsByClassName("date_li");

  for (var i = 0; i < dateLiElements.length; i++) {
    var eventLiElements = dateLiElements[i].getElementsByClassName("event_li");
    var dayMatch = false;

    for (var j = 0; j < eventLiElements.length; j++) {
      var eventString = normalizeString(eventLiElements[j].getElementsByClassName("searchstring")[0].textContent);
      var eventDateString = normalizeString(eventLiElements[j].getElementsByClassName("searchstring_date")[0].textContent);

      if (eventString.includes(filter) || eventDateString.includes(filter)) {
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
  var today = new Date();
  var t = today.getTime();
  var ul = document.getElementById("myUL");
  var li = ul.getElementsByClassName("event_li");

  for (var i = 0; i < li.length; i++) {
    var a = parseInt(li[i].getAttribute("data-begin_epoch"));
    var b = parseInt(li[i].getAttribute("data-end_epoch"));

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

  var today = new Date();
  var t = today.getTime();
  var ul = document.getElementById("myUL");
  var li = ul.getElementsByClassName("event_li");
  var currentEventFound = false;
  var nextEventElement = null;

  for (var i = 0; i < li.length; i++) {
    var a = parseInt(li[i].getAttribute("data-begin_epoch"));
    var b = parseInt(li[i].getAttribute("data-end_epoch"));

    if (b > t && t > a && !currentEventFound) {
      li[i].scrollIntoView({ behavior: "smooth", block: "center" });
      currentEventFound = true;
      hasScrolledInitially = true;
      break;
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
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  startTime();
  initialScrollToEvent();
});
