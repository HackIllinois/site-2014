(function(){
    $( document ).ready(function() {
        enableRetinaSponsorLogos();
    });

    /**
     * There's a weird bug in Safari that causes the retina logos to not show up until you mouse over them.
     * We have to do this weird CSS fix to make retina work at all, so we're just going to do that
     * in Chrome where the problem doesn't happen.
     */

    function enableRetinaSponsorLogos() {
        if (navigator.userAgent.indexOf('Chrome') != -1) {
            $('.sponsor, .sponsor-supernova').css('-webkit-transform', 'translateZ(0)');
        }
    }

})();
