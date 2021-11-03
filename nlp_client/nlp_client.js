import $ from "jquery";

var description = $("meta[name=description]").attr("content");
$("#output").html(description);
