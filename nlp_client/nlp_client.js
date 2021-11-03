/* eslint-disable no-undef*/

function getArray() {
  return $.getJSON("metatags.json");
}

getArray().done(function (json) {
  // now you can use json
  var questions = [];
  $.each(json.items, function (key, val) {
    var name = val.name;
    if ($("meta[name=" + name + "]").length) {
      console.log(name + "exist");
    } else {
      console.log(name + "does not exist");
    }
  });
});

var description = $("meta[name=description]").attr("content");
$("#output").html(description);
