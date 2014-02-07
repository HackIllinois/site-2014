$(document).ready(function() {

    $(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
       $(".launch-container").animate({
            marginLeft: "0px"
        }, {
            duration: 1000,
            easing: "linear"
        });
    }
    });

    var stratosphere = $(window).height();
    stratosphere+=500;
    stratosphere+='px';

    var form = $('#application');
    $('button#application-submit').click(function(event) {
        event.preventDefault();
        $(".rocket-plume").animate({
            opacity: 1,
            marginBottom: stratosphere
        }, {
            duration: 2050,
            easing: "easeInCirc",
            complete: function(){
                $('#application').submit();
            }
        });
        $(".rocket-ship").animate({
            marginBottom: stratosphere
        }, {
            duration: 2000,
            easing: "easeInCirc"
        });
    });
});