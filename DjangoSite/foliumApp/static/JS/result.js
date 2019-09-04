var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
var timeDurationList = {{ timeDurationList|safe }};
var tempData = {{ tempData|safe }};

// displaying intial time, date value for source mmsi
var sliderValueIndex = tempData.indexOf(Number(slider.value));
output.innerHTML = timeDurationList[sliderValueIndex];

slider.oninput = function() {
    output.innerHTML = timeDurationList[tempData.indexOf(Number(this.value))];
}

// getting values on value change from user and submitting to back-end
slider.onmouseup = function () {
  // getting user's input from demo elem and set it in form (hidden input) to submit values to back-end
  document.form.hiddenValue.value = document.getElementById("demo").innerHTML;
  document.getElementById("form").submit();
}

// slider support for mobile devices
slider.ontouchend = function () {
  // getting user's input from demo elem and set it in form (hidden input) to submit values to back-end
  document.form.hiddenValue.value = document.getElementById("demo").innerHTML;
  document.getElementById("form").submit();
}