var form_image = document.getElementById("profile");
var form_input = document.getElementById("file-input");
var form_input_d1 = document.getElementById("file-input-d1");
var form_input_d2 = document.getElementById("file-input-d2");

form_input.addEventListener("change", event => {
    // alert("changed");
    form_input_d1.setAttribute("value", form_input.value)
})