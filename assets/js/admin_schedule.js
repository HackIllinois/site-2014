$(document).ready(function() {

    // Character Counter for Description Box
    $("#inputDescription").on("change paste keydown keyup", function() {
      $("#char-count").text($("#inputDescription").val().length)
    });




    $("#render-feeditem").on('click', function(){

      var obj = {};
      obj.event_name = $("input[name='eventName']").val();
      obj.description = $("input[name='description']").val();
      obj.event_loc = $("input[name='eventLocation']").val();
      obj.img_src = getTypeUrl($("input[name='type']:checked"));
      obj.img_src = getTypeUrl($("input[name='day']:checked"));




      var card = createCard(obj);
      $("feed-container > ul").append(card);
    });

  });

function getTypeUrl(field){

  var def = "http://www.hackillinois.org/img/icons-iOS/hackillinois.png";
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
  var event_name = $("<p>").text(obj.event_name);
  var desc = $("<p>").text(obj.description);
  main_section.append(event_name);
  main_section.append(desc);

  var log_section = $("<section class='logistics col-md-2 pull-right'>")

  var location = $("<p>").text(obj.location);
  var time = $("<p>").text(obj.time);

  log_section.append(location);
  log_section.append(time);

  li.append(img_sec).append(main_section).append(log_section);
  return li;
}