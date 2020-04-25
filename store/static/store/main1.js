mqtt = new Paho.MQTT.Client("test.mosquitto.org", Number(8081), "sonoff-example-client");
mqtt.connect({onSuccess: function() {
console.log("connected!");
}});
// show the given page, hide the rest
var ele;
function show(elementID)
{
// try to find the requested page and alert if it's not found
ele = document.getElementById(elementID);
if (!ele) {
alert("no such element");
return;
}

// get all pages, loop through them and hide them
var pages = document.getElementById('home');
var pages1 = document.getElementById('home1');
pages.style.display = 'none';
pages1.style.display = 'none';
// then show the requested page
ele.style.display = 'block';
if(ele==home)
{
document.getElementById("status").innerHTML = "OFF";
message = new Paho.MQTT.Message("turn on");
}
else
{
document.getElementById("status").innerHTML = "ON";
message = new Paho.MQTT.Message("turn off");
}
// Send 'toggle' message to command topic
message.destinationName = "Jkuat-grid/house1/status";
mqtt.send(message);
}
