/* eslint-disable no-undef*/

function getConfig() {
  return $.getJSON("config.json");
}

function insertMetaTag(name, value) {
  console.log("inserting meta: name " + name + " value: " + value);
  $("head").append('<meta name="' + name + '" content="' + value + '">');
}

function get_tld(url) {
  var hostname = new URL(url).hostname;
  var tld = hostname.split(".").pop().toUpperCase();
  return tld;
}

function getParameters(json) {
  //{
  // now you can use json

  var elementToExtract = json.page.elementToExtract;
  console.log("elementToExtract: " + elementToExtract);
  var page_url = window.location.href;
  console.log("page url: " + page_url);
  var tld = get_tld(page_url);
  console.log("tld: " + tld);

  var metatagsArray = [];
  var includeOptionalTags = json.page.includeOptionalTags;
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
        } else if (val.hasOwnProperty("mapValue")) {
          if (name === "DC.ISO3166") {
            if (val.listOfValues.includes(tld)) {
              insertMetaTag(name, tld);
            } else {
              var obj = val.mapValue.find((o) => o.name === tld);
              console.log(obj);
              if (obj !== undefined) {
                tld = obj.value;
                insertMetaTag(name, tld);
              } else {
                metatagsArray.push(name);
              }
            }
          }
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
  callApi(page_url, elementToExtract, metatagsArray, json);
}

function callApi(page_url, elementToExtract, metatagsArray, json) {
  
  var base_url = json.api.baseurl;
  console.log("base url: " + base_url);
  var canenhance_url = base_url + "/" + json.api.operations[0].name;
  console.log("canenhance_url: " + canenhance_url);
  $.ajax({
    url: canenhance_url,
    method: json.api.operations[0].method,
    timeout: json.api.operations[0].timeout
  }).done(function (response1) {
    console.log(response1);
    if (response1.status) {
      var enhance_url = base_url + "/" + json.api.operations[1].name;
      console.log("enhance_url: " + enhance_url);

      var api_payload = json.api.operations[1].payload;
      console.log("api payload: " + api_payload);
      var text = $(elementToExtract).text().trim().replace(/\s+/g, " ");
      console.log("text: " + text);
      var request = api_payload
        .replace("$METATAGS$", JSON.stringify(metatagsArray))
        .replace("$URL$", JSON.stringify(page_url))
        .replace("$TEXT$", JSON.stringify(text));
      console.log(request);
      $.ajax({
        url: enhance_url,
        method: json.api.operations[1].method,
        timeout: json.api.operations[1].timeout,
        data: request,
        headers: {
          "Content-Type": "application/json"
        }
      }).done(function (response2) {
        console.log(response2);
        response2.metatags.forEach((element) => {
          insertMetaTag(element.name, element.value);
        });
      })
      .fail(function (jqXHR, textStatus) {
        if (textStatus === "timeout") {
          console.log("API timeout");
        }
      });
    }
  })
  .fail(function (jqXHR, textStatus) {
    if (textStatus === "timeout") {
      console.log("API timeout");
    }
  });
}

getConfig().done(function (json) {
  getParameters(json);
});

