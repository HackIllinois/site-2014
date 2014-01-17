$( document ).ready(function() {
    $(".reg-form").submit(function () {
        var email = $("input.reg-email").val();
        var email_check = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}$/i;
        if (!email_check.test(email)) {
            $('.reg-email').addClass("email-error");
            return false;
        }
        else {
            $.ajax({
                type: "POST",
                url: "",
                data: email,
                success: function () {
                    $(".reg-form").fadeOut("slow", function () {
                        $(".reg-success").fadeIn("slow");
                    });
                }
            });
            return false;
        }
    });
});

