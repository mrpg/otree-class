var ctid;

function tabshow(tid) {
    var tabbable = document.getElementsByClassName("tabbable");

    for (i = 0; i < tabbable.length; i++) {
        if (tabbable[i].id == "tabbable" + tid) {
            tabbable[i].style.display = "block";
        }
        else {
            tabbable[i].style.display = "none";
        }
    }

    var tab = document.getElementsByClassName("tab");

    for (i = 0; i < tab.length; i++) {
        if (tab[i].dataset.tab == tid) {
            tab[i].classList.remove("btn-secondary");
            tab[i].classList.add("btn-success");
        }
        else {
            tab[i].classList.remove("btn-success");
            tab[i].classList.add("btn-secondary");
        }
    }

    ctid = tid;

    $(window).scrollTop(0);
}

function tabinit() {
    var tabbable = document.getElementsByClassName("tabbable");

    for (i = 0; i < tabbable.length; i++) {
        if (tabbable[i].id == "tabbable1") {
            tabbable[i].innerHTML += "<p class='navbox'><span class='navright'><button onclick='right()' type='button' class='btn btn-primary'>Next</button></span></p>";
        }
        else if (tabbable[i].id == "tabbable" + tabbable.length) {
            tabbable[i].innerHTML += "<p class='navbox'><button onclick='left()' type='button' class='btn btn-secondary'>Back</button></p>";
        }
        else {
            tabbable[i].innerHTML += "<p class='navbox'><button onclick='left()' type='button' class='btn btn-secondary'>Back</button><span class='navright'><button onclick='right()' type='button' class='btn btn-primary'>Next</button></span></p>";
        }
    }

    var tab = document.getElementsByClassName("tab");

    for (i = 0; i < tab.length; i++) {
        tab[i].classList.add("btn");
        tab[i].classList.add("btn-secondary");

        tab[i].onclick = function (el) {
            tabshow(el.target.dataset.tab);
        };
    }
}

function left() {
    tabshow(parseInt(ctid)-1);
}

function right() {
    tabshow(parseInt(ctid)+1);
}
