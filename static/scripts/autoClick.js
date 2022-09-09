// setTimeout("CallButton()",10000)
// function CallButton()
// {
//    document.getElementById("button1").click();   
// }

var timeleft = 10;
var downloadTimer = setInterval(function(){
  if(timeleft <= 0){
    clearInterval(downloadTimer);
    document.getElementById("button1").innerHTML = "Next in (0s)";
    document.getElementById("button1").click(); 
  } else {
    document.getElementById("button1").innerHTML = "Next in (" + timeleft + "s)";
  }
  timeleft -= 1;
}, 1000);