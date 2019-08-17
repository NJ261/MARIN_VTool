var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
var timeDurationList = {{ timeDurationList|safe }};
var tempData = {{ tempData|safe }};
var sliderValueIndex = tempData.indexOf(Number(slider.value));
output.innerHTML = timeDurationList[sliderValueIndex];

slider.oninput = function() {
    output.innerHTML = timeDurationList[tempData.indexOf(Number(this.value))];
}

slider.onmouseup = function () {
  document.form.hiddenValue.value = document.getElementById("demo").innerHTML;
  document.getElementById("form").submit();
}

// slider support for mobile devices
slider.ontouchend = function () {
  document.form.hiddenValue.value = document.getElementById("demo").innerHTML;
  document.getElementById("form").submit();
}