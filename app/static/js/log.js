var modal = document.getElementById('logModal');

var blr = document.getElementById('blur')

var btn = document.getElementById('logBtn');

var closeBtn = document.getElementById('close');

btn.onclick = function(){
    modal.style.display = "block";
    blr.style.display = "block";   
}

closeBtn.onclick = function(){
    modal.style.display = "none";
    blr.style.display = "none";
}