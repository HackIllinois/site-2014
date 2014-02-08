(function(){
    $( document ).ready(function() {
        setupApplyButtonSlide();
        enableRetinaSponsorLogos();
    });

    function setupApplyButtonSlide() {
        $("#apply-btn-slide").on('click', function(){
            $("p.apply-info").slideDown(function(){
                $("a.apply-btn").attr("href","/apply");
            });

            $("#apply-btn-slide").text("continue");
            $("#apply-btn-slide").css('padding-left','96px');
            $("#apply-btn-slide").css('padding-right','96px');
        });
        $("a.apply-btn").attr("href","/apply");
    });
    }

    /**
     * There's a weird bug in Safari that causes the retina logos to not show up until you mouse over them.
     * We have to do this weird CSS fix to make retina work at all, so we're just going to do that
     * in Chrome where the problem doesn't happen.
     */
    function enableRetinaSponsorLogos() {
        if (navigator.userAgent.indexOf('Chrome') != -1) {
            console.log("applying css");
            $('.sponsor, .sponsor-supernova').css('-webkit-transform', 'translateZ(0)');
        }
    }

})();
