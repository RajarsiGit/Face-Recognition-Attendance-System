$(document).ready(function(){
  let namespace = "/video";
  let video = document.querySelector("#video");
  let canvas = document.querySelector("#myCanvas");
  let ctx = canvas.getContext('2d');
  video.style = "display: none !important;"
  var localMediaStream = null;
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  const h = 216;
  const w = 384;
  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }
    function myFunction(x) {
      if (x.matches) {
        ctx.canvas.width = h;
        ctx.canvas.height = w;
        ctx.drawImage(video, 0, 0, 720, 1280, 0, 0, h, w);
      } else {
        ctx.canvas.width = w;
        ctx.canvas.height = h;
        ctx.drawImage(video, 0, 0, 1280, 720, 0, 0, w, h);
      }
    }
    var x = window.matchMedia("(max-width: 600px)")
    myFunction(x);
    x.addListener(myFunction);
    let dataURL = canvas.toDataURL('image/jpeg');
    socket.emit('input', dataURL);
    console.log(video.videoHeight)
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
      width: {exact: 1280},
      height: {exact: 720}
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