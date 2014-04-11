$(document).ready(function() {

    // Character Counter for Description Box
    $("#inputDescription").on("change paste keydown keyup", function() {
      $("#char-count").text($("#inputDescription").val().length)
    });




    $("#render-feeditem").on('click', function(){

      var obj = {};
      obj.event_name = $("input[name='eventName']").val();
      obj.description = $("textarea[name='description']").val();
      obj.location = $("input[name='location']").val();
      obj.img_src = getTypeUrl($("input[name='type']:checked"));
      obj.day = getTypeUrl($("input[name='day']:checked"));

      //debugger;
      var card = createCard(obj);

      $(".feed-container > ul").prepend(card);
      debugger;
    });

  });

function getTypeUrl(field){

  var def = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZWVlIj48L3JlY3Q+PHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iMzIiIHk9IjMyIiBzdHlsZT0iZmlsbDojYWFhO2ZvbnQtd2VpZ2h0OmJvbGQ7Zm9udC1zaXplOjEycHg7Zm9udC1mYW1pbHk6QXJpYWwsSGVsdmV0aWNhLHNhbnMtc2VyaWY7ZG9taW5hbnQtYmFzZWxpbmU6Y2VudHJhbCI+NjR4NjQ8L3RleHQ+PC9zdmc+";
  //var def = "http://www.hackillinois.org/img/icons-iOS/hackillinois.png";
  var types = {
    "emergency" : "http://www.hackillinois.org/img/icons-iOS/emergency.png",
    "announcment" : "http://www.hackillinois.org/img/icons-iOS/announce.png",
  };

  return types[field.val()] || def;
}


//Awww yeeaaaa
function createCard(obj){

  var li = $("<li class='row event card'>");
  var img_sec = $("<section class='icon col-md-1'>");
  var img = $("<img class='media-object' style='width: 64px; height: 64px;''>");
  img.attr('src', obj.image_src)
  img_sec.append(img);

  var main_section = $("<section class='main-content col-md-6'>");
  var event_name = $("<p class='event-name'>").text(obj.event_name);
  var desc = $("<p class='description'>").text(obj.description);
  main_section.append(event_name).append(desc);

  var log_section = $("<section class='logistics col-md-2 pull-right'>")

  var location = $("<p>").text(obj.location);
  var time = $("<p>").text(obj.time);

  log_section.append(location).append(time);

  li.append(img_sec).append(main_section).append(log_section);
  return li;
}