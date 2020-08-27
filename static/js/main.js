$(document).ready(function(){
    let namespace = "/capture";
    let video = document.getElementById("video");
    let canvas = document.getElementById("myCanvas");
    let ctx = canvas.getContext('2d');
    ctx.canvas.width = 360;
    ctx.canvas.height = 240;
    var localMediaStream = null;
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    function sendSnapshot() {
        if (!localMediaStream) {
          return;
        }
        ctx.drawImage(video, 0, 0, 1280, 720, 0, 0, 360, 240);
        let dataURL = canvas.toDataURL('image/jpeg');
        socket.emit('capture', dataURL);
    }
    socket.on("message", function(data) {
        if(data.msg == 'Done') {
            window.location = location.protocol + '//' + document.domain + ':' + location.port + "/success_b";
        }
    });
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
    setInterval(function () {
        sendSnapshot();
    }, 50);
    })
    .catch(function(error) {
        console.log(error);
    });
});