// animate.CSS Default function
function animateCSS(element, animationName, callback) {
  const node = document.querySelector(element);
  node.classList.add("animated", animationName);
  function handleAnimationEnd() {
    node.classList.remove("animated", animationName);
    node.removeEventListener("animationend", handleAnimationEnd);

    if (typeof callback === "function") callback();
  }
  node.addEventListener("animationend", handleAnimationEnd);
}

var xmlhttp;

function handleResponse(response) {
  return response;
}
function sendData(url = ``, data = "", method = "POST") {
  if (method == "POST") {
    return fetch(url, {
      method: method, // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, cors, *same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, same-origin, *omit
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      redirect: "follow", // manual, *follow, error
      body: data, // body data type must match "Content-Type" header
    }).then((response) => handleResponse(response.json())); // parses response to JSON
  } else if (method == "GET") {
    return fetch(url + "?" + data).then((response) =>
      handleResponse(response.json())
    );
  }
}
if (window.XMLHttpRequest) {
  xmlhttp = new XMLHttpRequest();
} else {
  xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}
