var aas = document.querySelectorAll(".list-group-item-action");

for (let i = 0; i < aas.length; i++) {
    aas[i].addEventListener("click", function() {
        var productID = this.dataset.id;
        var sss = document.getElementsByClassName("list-group-item list-group-item-action active py-3 lh-sm");
        while (sss[0]) {
            sss[0].className = 'list-group-item list-group-item-action py-3 lh-sm"';
        }
        aas[i].className = 'list-group-item list-group-item-action active py-3 lh-sm';
        window.location.hash = `${productID}`;
        // alert(productID);
        //' d-flex align-items-center link-dark text-decoration-none dropdown-toggle';
    });
}


var sTags = document.querySelectorAll('.tabs');
for (let i = 0; i < sTags.length; i++) {
    sTags[i].addEventListener("click", function() {
        var idTarget = this.dataset.tg;
        // alert(`clicked ${idTarget}`);
        var sss = document.getElementsByClassName("tab-pane active show");
        // while (sss[0]) {
        //     sss[0].className = 'tab-pane"';
        // }
        for (let j = 0; j < sss.length; j++) {
            sss[0].className = 'tab-pane"';
        }
        const itemTag = document.getElementById(idTarget);
        itemTag.className = 'tab-pane active show';
        // aas[i].className = 'tab-pane active show';
        //' d-flex align-items-center link-dark text-decoration-none dropdown-toggle';
    });
}

const height = document.querySelector("#height span");
const width = document.querySelector("#width span");

// Insert values on load of page
window.onload = function() {
    height.innerHTML = window.innerHeight;
    width.innerHTML = window.innerWidth;
};

// Change values when window is resized
var menu_side_bar = document.getElementById('menu_side_bar');
var divider_side_bar = document.getElementById('b-example-divider');
window.onresize = resize;

function resize() {
    if (window.innerWidth < 768) {

        // alert("resize event detected!");
        menu_side_bar.remove();
    }
}

if (window.innerWidth < 768) {

    // alert("resize event detected!");
    menu_side_bar.remove();
    divider_side_bar.remove();
}


const completeModule = (pk) => {

    fetch(url_send_data, {
            method: "POST",
            // credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,

                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: JSON.stringify({
                module_id: pk,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            // console.log(data);
            // alert(data.message);

            location.reload();

            alertify.success(data.message);



        });
}

function getCookie(name) {
    let csrftoken = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                csrftoken = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return csrftoken;
}

var csrftoken = getCookie('csrftoken');

var like_un_like = document.querySelectorAll(".like_un_like");

for (let i = 0; i < like_un_like.length; i++) {
    like_un_like[i].addEventListener("click", function() {
        var productID = this.dataset.id;
        // alert(`clicked ${productID}`);
        completeModule(productID);



        //' d-flex align-items-center link-dark text-decoration-none dropdown-toggle';
    });
}