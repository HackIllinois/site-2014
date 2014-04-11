var rooms = [{'building':'Siebel', 'floor':'Basement', 'room_number':'SC 0216', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'Basement', 'room_number':'SC 0224', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'Basement', 'room_number':'SC Basement', 'room_type':'hacker space' ,'room_name':'Basement Open Space', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1103', 'room_type':'sleep room' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1105', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1109', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1112', 'room_type':'game room' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1131', 'room_type':'game room' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1214', 'room_type':'sleep room' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1302', 'room_type':'Interactive Intelligence room' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1304', 'room_type':'Special sponsor room' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1404', 'room_type':'Kickoff and Tech Talks' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC Atrium', 'room_type':'sponsor tables and food serving' ,'room_name':'1st Floor Atrium', 'image_url':''},
{'building':'Siebel', 'floor':'1', 'room_number':'SC 1312', 'room_type':'Mission Control Annex' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'2', 'room_number':'SC 2405', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'2', 'room_number':'SC 2235', 'room_type':'sponsor interview' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'2', 'room_number':'SC 2237', 'room_type':'sponsor interview' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'2', 'room_number':'SC 2nd Atrium', 'room_type':'sponsor tables' ,'room_name':'2nd floor Atrium', 'image_url':''},
{'building':'Siebel', 'floor':'2', 'room_number':'SC 2102', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'2', 'room_number':'SC 2124', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'2', 'room_number':'SC 2407', 'room_type':'Mission Control' ,'room_name':'Mission Control', 'image_url':''},
{'building':'Siebel', 'floor':'3', 'room_number':'SC 3401', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'3', 'room_number':'SC 3403', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'3', 'room_number':'SC 3405', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'3', 'room_number':'SC 3102', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'3', 'room_number':'SC 3124', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'4', 'room_number':'SC 4102', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'4', 'room_number':'SC 4124', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'4', 'room_number':'SC 4403', 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'4', 'room_number':'SC 4405', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'Siebel', 'floor':'4', 'room_number':'SC 4407', 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
{'building':'DCL', 'floor':'1', 'room_number':'DCL 1310', 'room_type':'tech talks' ,'room_name':'', 'image_url':''},
{'building':'DCL', 'floor':'1', 'room_number':'DCL 1320', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
{'building':'DCL', 'floor':'2', 'room_number':'DCL 2320', 'room_type':'hardware hacker space' ,'room_name':'', 'image_url':''},
{'building':'DCL', 'floor':'2', 'room_number':'DCL 2436', 'room_type':'hardware hacker space' ,'room_name':'', 'image_url':''}];


$(document).ready(function() {


  var companyNames = [
  '3red',
  'a16z',
  'allston',
  'announce',
  'answers',
  'ba',
  'bloomberg',
  'citadel',
  'dropbox',
  'electricimp',
  'element',
  'emergency',
  'epic',
  'etsy',
  'firebase',
  'ge',
  'goldman',
  'google',
  'groupon',
  'hackillinois',
  'hudl',
  'imo',
  'inin',
  'johndeere',
  'kcg',
  'kohls',
  'mailgun',
  'makerlab',
  'neustar',
  'niksun',
  'octopart',
  'onenorth',
  'pebble',
  'rdio',
  'spark',
  'sparkfun',
  'spiceworks',
  'spot',
  'statefarm',
  'tata',
  'trunkclub',
  'twilio',
  'venmo',
  'westmonroe',
  'wolfram',
  'yahoo',
  ];

  //RELEASE THE BLOODHOUND!!
  var companiesHound = new Bloodhound({
    datumTokenizer: function(d) {
      return Bloodhound.tokenizers.whitespace(d.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: companyNames.map(function(c) {
      return { value: c };
    })
  });

  var roomsHound = new Bloodhound({
    datumTokenizer: function(d) {
      return Bloodhound.tokenizers.whitespace(d.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: rooms.map(function(r){
      return { value: r['room_number']};
    })
  });

// kicks off the loading/processing of `local` and `prefetch`
companiesHound.initialize();
roomsHound.initialize();

$("#bloodhound input[name='company']").typeahead({
  hint: false,
  highlight: false,
  minLength: 1
},
{
  name: 'companies',
  displayKey: 'value',
  // `ttAdapter` wraps the suggestion engine in an adapter that
  // is compatible with the typeahead jQuery plugin
  source: companiesHound.ttAdapter()
});
$("#bloodhound input[name='location']").typeahead({
  hint: false,
  highlight: false,
  minLength: 1
},
{
  name: 'room',
  displayKey: 'value',
  // `ttAdapter` wraps the suggestion engine in an adapter that
  // is compatible with the typeahead jQuery plugin
  source: roomsHound.ttAdapter()
});



    // Character Counter for Description Box
    $("#inputDescription").on("change paste keydown keyup", function() {
      $("#char-count").text($("#inputDescription").val().length);
    });



    $("#render-feeditem").on('click', function(){

      var obj = parseForm();
      var card = createCard(obj);

      $(".feed-container > ul").prepend(card);
    });


    $("button[type='submit']").click(function(){
      //send post
      $.post({
        url: window.location.pathname,
        data: parseForm(),
        success: function(data, status){
          alert(status);
          //clear form fields
          $("input[name='eventName']").val('');
          obj.description = $("textarea[name='description']").val('');
          obj.location = $("input[name='location']").val('');
        }
      });

      //clear fields

    });

    function parseForm(){
      var obj = {};
      obj.event_name = $("input[name='eventName']").val();
      obj.description = $("textarea[name='description']").val();
      obj.location = $("input[name='location']").val();
      obj.img_src = getTypeUrl($("input[name='company']"));
      obj.day = getTypeUrl($("input[name='day']:checked"));
      obj.time = moment().format('HH:mm:ss');

      return obj;
    }


  });

function getTypeUrl(field){

  var def = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZWVlIj48L3JlY3Q+PHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iMzIiIHk9IjMyIiBzdHlsZT0iZmlsbDojYWFhO2ZvbnQtd2VpZ2h0OmJvbGQ7Zm9udC1zaXplOjEycHg7Zm9udC1mYW1pbHk6QXJpYWwsSGVsdmV0aWNhLHNhbnMtc2VyaWY7ZG9taW5hbnQtYmFzZWxpbmU6Y2VudHJhbCI+NjR4NjQ8L3RleHQ+PC9zdmc+";
  //var def = "http://www.hackillinois.org/img/icons-iOS/hackillinois.png";
  if( !field.val() ){
    return def;
  }
  else return "/img/icons-iOS/" + field.val().toLowerCase() + ".png"
}


//Awww yeeaaaa
function createCard(obj){

  var li = $("<li class='row event card'>");
  var img_sec = $("<section class='icon col-md-1'>");
  var img = $("<img class='media-object' style='width: 64px; height: 64px;''>");
  img.attr('src', obj.img_src);
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