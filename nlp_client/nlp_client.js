/* eslint-disable no-undef*/

function getConfig() {
  return $.getJSON("config.json");
}

function insertMetaTag(name, value) {
  console.log("[NLP-POC] inserting metatag " + name + " with value: " + value);
  $("head").append('<meta name="' + name + '" content="' + value + '">');
}

function get_topleveldomain(url) {
  var hostname = new URL(url).hostname;
  var tld = hostname.split(".").pop().toUpperCase();
  return tld;
}

function getParameters(json) {

  var page_url = window.location.href;
  var tld = get_topleveldomain(page_url);

  var metatagsArray = [];
  var includeOptionalTags = json.page.includeOptionalTags;
  $.each(json.metatags, function (key, val) {
    var name = val.name;
    if ($("meta[name='" + name + "']").length) {
      console.log("[NLP-POC] " + name + " exist");
    } else {
      console.log("[NLP-POC] " + name + " does not exist");

      var mandatory = val.mandatory;
      if (mandatory) {
        console.log("[NLP-POC] " + name + " is mandatory");
        if (Object.prototype.hasOwnProperty.call(val, "expectedValue")) {
          console.log("[NLP-POC] " + val.expectedValue + " is expected");
          insertMetaTag(name, val.expectedValue, );
        } else if (Object.prototype.hasOwnProperty.call(val, "mapValue")) {
          if (name === "DC.ISO3166") {
            if (val.listOfValues.includes(tld)) {
              insertMetaTag(name, tld);
            } else {
              var obj = val.mapValue.find((o) => o.name === tld);
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
          console.log("[NLP-POC] " + name + " is optional but requested.");
          if (Object.prototype.hasOwnProperty.call(val, "expectedValue")) {
            console.log("[NLP-POC] " + val.expectedValue + " is expected");
            insertMetaTag(name, val.expectedValue);
          } else {
            metatagsArray.push(name);
          }
        } else {
          console.log("[NLP-POC] " + name + " is not mandatory and not requested");
        }
      }
    }
  });

  console.log("[NLP-POC] These metatags are then needed: " + JSON.stringify(metatagsArray));
  callApi(page_url, metatagsArray, json);
}

function callApi(page_url, metatagsArray, json) {
  
  var base_url = json.api.baseurl;

  var canenhance_url = base_url + "/" + json.api.operations[0].name;
  console.log("[NLP-POC] Contacting API: " + canenhance_url);

  $.ajax({
    url: canenhance_url,
    method: json.api.operations[0].method,
    timeout: json.api.operations[0].timeout
  }).done(function (response1) {
    console.log("[NLP-POC] Response: " + JSON.stringify(response1));
    if (response1.status) {
      
      var enhance_url = base_url + "/" + json.api.operations[1].name;
      console.log("[NLP-POC] Contacting API: " + enhance_url);

      var elementToExtract = json.page.elementToExtract;
      var content = $(elementToExtract).clone();
      content.find('script').remove();
      content.find('noscript').remove();
      var text = content.text().trim().replace(/\s+/g, " ");

      var api_payload = json.api.operations[1].payload;
      var request = api_payload
        .replace("$METATAGS$", JSON.stringify(metatagsArray))
        .replace("$URL$", JSON.stringify(page_url))
        .replace("$TEXT$", JSON.stringify(text));
      console.log("[NLP-POC] request: " + request);

      $.ajax({
        url: enhance_url,
        method: json.api.operations[1].method,
        timeout: json.api.operations[1].timeout,
        data: request,
        headers: {
          "Content-Type": "application/json"
        }
      }).done(function (response2) {
        console.log("[NLP-POC] Response: " + JSON.stringify(response2));
        response2.metatags.forEach((element) => {
          if(element.value !==  json.api.operations[1].notimplemented && 
             element.value !==  json.api.operations[1].notfound &&
             element.value !== "") {
            insertMetaTag(element.name, element.value);
        }
        });
      })
      .fail(function (jqXHR, textStatus) {
        if (textStatus === "timeout") {
          console.log("[NLP-POC] API timeout");
        }
      });
    }
  })
  .fail(function (jqXHR, textStatus) {
    if (textStatus === "timeout") {
      console.log("[NLP-POC] API timeout");
    }
  });
}

getConfig().done(function (json) {
  getParameters(json);
});

