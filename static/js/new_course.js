var img_thumb = document.getElementById("course_thumb")
var new_course = document.getElementById("course_new")

img_thumb.addEventListener("load", (event) => {
    alert('loaded');
})

new_course.addEventListener("submit", (event) => {
    event.preventDefault();
    alert("alerting");
})