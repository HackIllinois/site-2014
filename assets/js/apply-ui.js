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
    stratosphere+=100;
    stratosphere+='px';

    $(".launcher-btn").on('click', function(){
        $(".rocket-plume").animate({
            opacity: 1
        }, {
            duration: 1500,
            easing: "easeOutSine"
        });
        $(".rocket-plume").animate({
            marginBottom: stratosphere
        }, {
            duration: 10000,
            easing: "easeInBounce"
        });
        $(".rocket-ship").animate({
            marginBottom: stratosphere
        }, {
            duration: 10000,
            easing: "easeInBounce"
        });
    });
});
