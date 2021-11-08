/* eslint-disable no-undef*/

function getConfig() {
  return $.getJSON("config.json");
}

function insertMetaTag(name, value) {
  $("head").append('<meta name="' + name + '" content="' + value + '">');
}

function getParameters(json) {
  //{
  // now you can use json
  var includeOptionalTags = json.page.includeOptionalTags;
  var metatagsArray = [];
  $.each(json.metatags, function (key, val) {
    var name = val.name;
    if ($("meta[name='" + name + "']").length) {
      console.log(name + " exist");
    } else {
      console.log(name + " does not exist");

      var mandatory = val.mandatory;
      if (mandatory) {
        console.log(name + " is mandatory");
        if (val.hasOwnProperty("expectedValue")) {
          console.log(val.expectedValue + " is expected");
          insertMetaTag(name, val.expectedValue);
        } else {
          metatagsArray.push(name);
        }
      } else {
        if (includeOptionalTags) {
          console.log(name + " is optional but requested");
          if (val.hasOwnProperty("expectedValue")) {
            console.log(val.expectedValue + " is expected");
            insertMetaTag(name, val.expectedValue);
          } else {
            metatagsArray.push(name);
          }
        } else {
          console.log(name + " is not mandatory and not requested");
        }
      }
    }
  });

  $.each(metatagsArray, function (i, val) {
    console.log(val + " is due");
  });
  var elementToExtract = json.page.elementToExtract;
  console.log("elementToExtract: " + elementToExtract);
  var api_payload = json.api.payload;
  console.log("api payload: " + api_payload);
  var api_url = json.api.url;
  console.log("api url: " + api_url);
  callApi(metatagsArray, elementToExtract, api_payload, api_url);
}

function callApi(metatagsArray, elementToExtract, api_payload, api_url) {
  var page_url = window.location.href;
  var text = $(elementToExtract).text().trim().replace(/\s+/g, " ");
  var request = api_payload
    .replace("$METATAGS$", JSON.stringify(metatagsArray))
    .replace("$URL$", JSON.stringify(page_url))
    .replace("$TEXT$", JSON.stringify(text));
  /*var sendJson = {
    metatags: metatagsArray,
    url: page_url,
    text: text
  };
  console.log(JSON.stringify(sendJson));
  */
  console.log(request);
}

getConfig().done(function (json) {
  getParameters(json);
});
/* script.js
var yourObject = {
  test:'test 1',
  testData: [ 
    {testName: 'do',testId:''}
   ],
   testRcd:'value'   
};
var myString = 'newData='+JSON.stringify(yourObject);  //converts json to string and prepends the POST variable name
$.ajax({
   type: "POST",
   url: "buildJson.php", //the name and location of your php file
   data: myString,      //add the converted json string to a document.
   success: function() {alert('sucess');} //just to make sure it got to this point.
});
return false; 

buildJson.php

<?php
    $file = "data.json";  //name and location of json file. if the file doesn't exist, it   will be created with this name

    $fh = fopen($file, 'a');  //'a' will append the data to the end of the file. there are other arguemnts for fopen that might help you a little more. google 'fopen php'.

    $new_data = $_POST["newData"]; //put POST data from ajax request in a variable

    fwrite($fh, $new_data);  //write the data with fwrite

    fclose($fh);  //close the dile
?>
*/
