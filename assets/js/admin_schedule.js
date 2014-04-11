$(document).ready(function() {
  alert("GUCCI");

    // $("#addFeedItem-form").submit(function(event) { });
    $("#inputDescription").on("change paste keydown keyup", function() {
      $("#char-count").text($("#inputDescription").val().length)
    });
    $("#addFeedItem-button").click(function() {
      $(".feedform-container").slideToggle();
      $(".rendered-container").slideUp();
    });

    $("#render-feeditem").click(function() {
      if ($("#inputDescription").val() && $("input[name='type']:checked").val()) {
        type = $("input[name='type']:checked").val();
        if (type == "emergency") {
          $("#rendered-image").attr('src','http://www.hackillinois.org/img/icons-iOS/emergency.png');
          $("#rendered-image").attr('alt','emergency');
        } else if (type == "announcement") {
          $("#rendered-image").attr('src','http://www.hackillinois.org/img/icons-iOS/announce.png');
          $("#rendered-image").attr('alt','announce');
        } else {
          $("#rendered-image").attr('src','http://www.hackillinois.org/img/icons-iOS/hackillinois.png');
          $("#rendered-image").attr('alt','hackillinois');
        }
        $("#rendered-description").html($("#inputDescription").val());
        $(".rendered-container").slideDown();
      } else {
        alert("Please fill in the 'Description' and 'Type'.");
      }
    // $("#inputHighlights")
  });


  }