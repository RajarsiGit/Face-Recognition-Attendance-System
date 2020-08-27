$(document).ready(function(){
    let video = document.getElementById("video");
    let submitInput = document.getElementById("submit");
    submitInput.style = "float: none !important; margin: 15px 25% 15px 25%; !important; "
    let emailInput = document.getElementById("id");
    emailInput.setAttribute("placeholder", "Enter ID");
    var localMediaStream = null;
    var constraints = {
        audio: false,
        video: {
            width: {max: 1280},
            height: {max: 720}
        }
    };
    navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
        video.srcObject = stream;
        localMediaStream = stream;
    })
    .catch(function(error) {
        console.log(error);
    });
});