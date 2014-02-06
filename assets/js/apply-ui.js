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

    $(".launcher-btn").on('click', function(){
        $(".rocket-plume").animate({
            opacity: 1,
            marginBottom: stratosphere
        }, {
            duration: 2050,
            easing: "easeInCirc"
        });
        $(".rocket-ship").animate({
            marginBottom: stratosphere
        }, {
            duration: 2000,
            easing: "easeInCirc"
        });
    });
});
