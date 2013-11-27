var email = $("input.reg-email").val();
$(".send").click(function() {  
    $.ajax({  
    type: "POST",  
    url: "/",  
    data: email,  
    success: function() {  
        $(".reg-form").fadeOut( "slow", function() {
            $(".reg-container").append("<h3>You're all set! We'll be in touch soon.</h3>");
        });
    }  
    });  
return false;   
});

