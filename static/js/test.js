$(document).ready(function(){
  let namespace = "/video";
  let video = document.querySelector("#video");
  let canvas = document.querySelector("#myCanvas");
  let ctx = canvas.getContext('2d');
  video.style = "display: none !important;"
  ctx.canvas.width = 240;
  ctx.canvas.height = 180;
  var localMediaStream = null;
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }
    ctx.drawImage(video, 0, 0, 1280, 720, 0, 0, 240, 180);
    let dataURL = canvas.toDataURL('image/jpeg');
    socket.emit('input', dataURL);
  }
  socket.on("message", function(data) {
    if(data.msg == 'Done') {
      window.location = location.protocol + '//' + document.domain + ':' + location.port + "/success_a";
    }
    $("#image").attr('src', 'data:image/jpeg;base64,' + data.msg)
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
    }, 60);
  })
  .catch(function(error) {
    console.log(error);
  });
});