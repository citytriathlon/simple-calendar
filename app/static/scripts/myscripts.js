var HIGHLIGHT_INTERVAL_MS = 10000;

function normalizeString(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toUpperCase();
}

function filterEvents() {
  var input = document.getElementById("myInput");
  var ul = document.getElementById("myUL");
  if (!input || !ul) return;

  var filter = normalizeString(input.value);
  var dateLiElements = ul.getElementsByClassName("date_li");

  for (var i = 0; i < dateLiElements.length; i++) {
    var eventLiElements = dateLiElements[i].getElementsByClassName("event_li");
    var dayMatch = false;

    for (var j = 0; j < eventLiElements.length; j++) {
      var eventString =
        eventLiElements[j].getElementsByClassName("searchstring")[0].textContent;
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

function eventRows() {
  var ul = document.getElementById("myUL");
  return ul ? ul.getElementsByClassName("event_li") : [];
}

function epochOf(row, className) {
  var node = row.getElementsByClassName(className)[0];
  return node ? parseInt(node.innerText, 10) : NaN;
}

function highlightCurrentEvents() {
  var now = Date.now();
  var rows = eventRows();

  for (var i = 0; i < rows.length; i++) {
    var begin = epochOf(rows[i], "begin_epoch");
    var end = epochOf(rows[i], "end_epoch");

    if (now > begin && now < end) {
      rows[i].style.backgroundColor = "lightblue";
    } else {
      rows[i].style.backgroundColor = now > end ? "lightgray" : "";
    }
  }

  setTimeout(highlightCurrentEvents, HIGHLIGHT_INTERVAL_MS);
}

function scrollToRelevantEvent() {
  var now = Date.now();
  var rows = eventRows();
  var nextEventElement = null;

  for (var i = 0; i < rows.length; i++) {
    var begin = epochOf(rows[i], "begin_epoch");
    var end = epochOf(rows[i], "end_epoch");

    if (now > begin && now < end) {
      rows[i].scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }
    if (begin > now && !nextEventElement) {
      nextEventElement = rows[i];
    }
  }

  if (nextEventElement) {
    nextEventElement.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

function toggleDescription(row) {
  // Only rows with a description or location get a panel rendered.
  var content = row.nextElementSibling;
  if (!content || content.className.indexOf("description") === -1) return;

  var isOpen = content.style.display === "block";
  content.style.display = isOpen ? "none" : "block";
  row.classList.toggle("active", !isOpen);
  row.setAttribute("aria-expanded", isOpen ? "false" : "true");
}

function wireExpanders() {
  var rows = document.getElementsByClassName("events-vert");

  for (var i = 0; i < rows.length; i++) {
    if (rows[i].getAttribute("role") !== "button") continue;

    rows[i].addEventListener("click", function () {
      toggleDescription(this);
    });

    rows[i].addEventListener("keydown", function (event) {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      toggleDescription(this);
    });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  var input = document.getElementById("myInput");
  if (input) input.addEventListener("input", filterEvents);

  wireExpanders();
  highlightCurrentEvents();
  scrollToRelevantEvent();
});
