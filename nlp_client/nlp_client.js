/* eslint-disable no-undef*/

function getArray() {
  return $.getJSON("metatags.json");
}

var notexist = [];
getArray().done(function (json) {
  // now you can use json
  $.each(json.items, function (key, val) {
    var name = val.name;
    if ($("meta[name='" + name + "']").length) {
      console.log(name + " exist");
    } else {
      console.log(name + " does not exist");
      var mandatory = val.mandatory;
      if (mandatory) {
        console.log(name + " is mandatory");
        notexist.push(name);
      } else {
        console.log(name + " is not mandatory");
      }
    }
  });
  callapi(notexist);
});

function callapi(notexistArray) {
  $.each(notexistArray, function (i, val) {
    console.log(val + " is due");
  });
  var description = $("meta[name=description]").attr("content");
  $("#output").html(description);
}
