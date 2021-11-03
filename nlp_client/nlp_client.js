function getArray() {
  return $.getJSON("metatags.json");
}

getArray().done(function (json) {
  // now you can use json
  var questions = [];
  $.each(json.items, function (key, val) {
    var name = val.name;
    console.log(name);
  });
});

var description = $("meta[name=description]").attr("content");
$("#output").html(description);
