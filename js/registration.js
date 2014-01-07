function $(elid){
    return document.getElementById(elid);
}

var cursor;
window.onload = init;
function init(){
    cursor = $("cursor");
    cursor.style.left = "0px";
}

function nl2br(txt){
    return txt.replace(/\n/g, "<br />");
}

function writeit(from, e){
    e = e || window.event;
    var w = $("writer");
    var tw = from.value;
    w.innerHTML = nl2br(tw);
}

function moveIt(count, e){
    e = e || window.event;
    var keycode = e.keyCode || e.which;
    if(keycode == 37 && parseInt(cursor.style.left) >= (0-((count-1)*10))){
        cursor.style.left = parseInt(cursor.style.left) - 10 + "px";
    } else if(keycode == 39 && (parseInt(cursor.style.left) + 10) <= 0){
        cursor.style.left = parseInt(cursor.style.left) + 10 + "px";
    }
    if(e.ctrlKey && e.keyCode == 65){
        $("writer").style.backgroundColor = "#99ccff";
    } else {
        $("writer").style.backgroundColor = "";
    }
}

function alert(txt){
    console.log(txt);
}