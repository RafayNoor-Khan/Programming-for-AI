document.addEventListener("DOMContentLoaded", function() {
    fetch("/apod")
    .then(response => response.json())
    .then(data => {
        document.getElementById("title").innerText = data.title;
        document.getElementById("apod-image").src = data.url;
        document.getElementById("explanation").innerText = data.explanation;
    })
    .catch(error => console.error("Error fetching APOD:", error));
});
