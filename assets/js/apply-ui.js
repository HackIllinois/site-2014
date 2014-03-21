function validateApplication() {

    if (
        $("#nameFirst").val().length == 0 ||
        $("#nameLast").val().length == 0 ||
        $("#email").val().length == 0 ||
        $("#school").val().length == 0 ||
        $("#experience").val().length == 0) {
        return false;
    } else if (!$("input[name='gender']:checked").val()) {
        return false;
    } else if (!$("input[name='year']:checked").val()) {
        return false;
    } else if (!$("input[name='shirt']:checked").val()) {
        return false;
    } else if (!$("input[name='travel']:checked").val()) {
        return false;
    } else if ($("input[name='travel']:checked").val().indexOf('bus') != -1 && $("select[name='busRoute'] option:selected").text().indexOf("select") != -1) {
        return false;
    } else {
        return true;
    }

}

$(document).ready(function () {

    if (!$('#termsOfService-0').prop('checked') == true) {
        checkedTC = false;
        $('#application-submit').attr("disabled", "disabled");
        $('#application-submit').addClass("submit-disabled");
    }

    $('#termsOfService-0').on('click', function () {
        if ($('#termsOfService-0').prop('checked')) {
            $('#application-submit').removeAttr('disabled');
            $('#application-submit').removeClass("submit-disabled");
        } else {
            $('#application-submit').attr("disabled", "disabled");
            $('#application-submit').addClass("submit-disabled");

        }
    });

    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() == $(document).height()) {
            $(".launch-container").animate({
                marginLeft: "0px"
            }, {
                duration: 1000,
                easing: "linear"
            });
        }
    });

    var form = $('#application');
    $('button#application-submit').click(function (event) {
        event.preventDefault();
        var stratosphere = $(window).height();
        stratosphere += 150;
        stratosphere += 'px';

        if (validateApplication()) {
            $(".rocket-ship").animate({
                marginBottom: stratosphere
            }, {
                duration: 2000,
                easing: "easeInCirc"
            });
            $(".rocket-plume").animate({
                opacity: 1,
                marginBottom: stratosphere
            }, {
                duration: 2050,
                easing: "easeInCirc",
                complete: function () {
                    $('#application').submit();
                }
            });
        } else {
            $('.field-missing').show();
            $('html, body').animate({
                scrollTop: ($('.field-missing').first().offset().top - 30)
            }, 500);
        }
    });
});
