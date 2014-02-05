(function(){
    $( document ).ready(function() {
        $("#apply-btn-slide").on('click', function(){
        
            $("p.apply-info").slideDown(function(){
                $("a.apply-btn").attr("href","/apply");
            });

            $("#apply-btn-slide").text("continue");
            $("#apply-btn-slide").css('padding-left','96px');
            $("#apply-btn-slide").css('padding-right','96px');
        });

})();

