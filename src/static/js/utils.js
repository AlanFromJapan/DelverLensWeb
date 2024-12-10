/**
 * Functions useful for the site in one JS to save on page sizes (save the electrons!)
 * 
 * 
*/

//Adds a confirmation popup before submitting the form (or just submit if pmessage == '')
function clickConfirm(pname, pvalue, pmessage="Sure ?") {
    if (pmessage == '' || confirm(pmessage)){
        var f = document.getElementById('theForm');

        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = pname;
        hiddenField.value = pvalue;

        f.appendChild(hiddenField);
        f.submit();
    }
}



//changes the language
function switchLanguage(l){

    //https://stackoverflow.com/questions/36975619/how-to-call-a-rest-web-service-api-from-javascript
    var xhttp = new XMLHttpRequest();
    // xhttp.onreadystatechange = function() {
    //         if (this.readyState == 4 && this.status == 200) {
    //         var d = document.getElementById('currentstatus');
    //         d.innerHTML = this.responseText.replace('\n', '<br/>');
    //         }
    // };
    xhttp.open("PUT", "api/language/" + l, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}

//changes the letter style
function switchLetterStyle(l){

    //https://stackoverflow.com/questions/36975619/how-to-call-a-rest-web-service-api-from-javascript
    var xhttp = new XMLHttpRequest();
    // xhttp.onreadystatechange = function() {
    //         if (this.readyState == 4 && this.status == 200) {
    //         var d = document.getElementById('currentstatus');
    //         d.innerHTML = this.responseText.replace('\n', '<br/>');
    //         }
    // };
    xhttp.open("PUT", "api/letterstyle/" + l, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}


//changes the letter case
function switchLetterCase(l){

    //https://stackoverflow.com/questions/36975619/how-to-call-a-rest-web-service-api-from-javascript
    var xhttp = new XMLHttpRequest();
    // xhttp.onreadystatechange = function() {
    //         if (this.readyState == 4 && this.status == 200) {
    //         var d = document.getElementById('currentstatus');
    //         d.innerHTML = this.responseText.replace('\n', '<br/>');
    //         }
    // };
    xhttp.open("PUT", "api/lettercase/" + l, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}

var lastAudio = null;

//plays the audio for the text
function speech2textAPI(lang, text){
    var url = "api/speech2text/" + lang + "/" + text;
    const audioElement = new Audio(url);
    audioElement.play();

    lastAudio = audioElement;
}

function replayLatestAudio(){
    if (lastAudio != null){
        lastAudio.play();
    }
}

//returns the shuffled version of a word
function shuffle (s) {
    var a = s.split(""),
        n = a.length;

    for(var i = n - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
    }
    return a.join("");
}


//Score API functions
function callScoreAPI(action, game){

    //https://stackoverflow.com/questions/36975619/how-to-call-a-rest-web-service-api-from-javascript
    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", "api/score/" + action + "/" + game, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}