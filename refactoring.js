//Current Selected Physician
var node_value = document.getElementById('physician').value

function update() {
  //Starting with new array
  var taken_schedules = Array(0)
  //Looping with Jinja to get physician Schedule Data (All Physicians for a given hopsital > start time)
  {% for events in physician_schedule %}
    //If Selected physician (node_value)
    {% if events.user_id == node_value %}
      //Pushes Dates of specific function to taken_schedules
      taken_schedules.push("{{events.start_time}}")
    {% endif %}
  {% endfor %}
  //Moment Array, Curr Month
  //Formatting current date for comparisons
  var moment_array = Array(0)
  //Getting current attributes
  var curr_month = moment().format("MM")
  var curr_year = moment().format("YYYY")
  var curr_day = moment().format("DD")
  var now_time = moment(curr_year + "-" + curr_month + "-" + curr_day + " " + "07:00:00", "YYYY-MM-DD HH:mm:ss")
  // Last Day of Month
  var quit = parseFloat(moment().endOf("month").format("D"))
  //Calculating/Getting available appointment Time Slots (getting all 30-minute time slots in the current month)
  for(i = 0; i < quit; i++) {
    if (i != 0){
    //
    now_updated = now_time.add(1, "days").subtract(11, "hours")
  } else {
    var now_updated = now_time
  }
    for(j=0; j < 22 ; j++){
      now_updated = now_updated.add(30,'minutes')
      moment_array.push(now_updated.format("YYYY-MM-DD HH:mm:ss"))
    }
  }
  //Gets available Time slots as the difference of array 1 from array 2
  var new_array = Array(0)
  for(i = 0; i < moment_array.length; i++){
    if (taken_schedules.indexOf(moment_array[i]) == -1)  {
      new_array.push(moment_array[i])
    }
  }
  //Populates Selected Field with available Time Slots
  var selected = document.getElementById('time_slot')
  var length = selected.options.length;
  //Clears current selection
  while (selected.firstChild){
    selected.removeChild(selected.firstChild)
  }
  //Sets Selection to new options for elements in new_array
  for (i = 0; i < new_array.length; i++){
    selected.options[selected.options.length] = new Option(new_array[i] + " to " + moment(new_array[i], "YYYY-MM-DD HH:mm:ss").add(30, "minutes").format("YYYY-MM-DD HH:mm:ss"), i)
  }
}
