function approveBusRoutes() {
    $('#travel-0').on('click', function () {
		if($("select[name='busRoute']").val() != ""){
			$('#rsvp-submit-btn').removeAttr('disabled');
			$('#rsvp-submit-btn').removeClass("submit-disabled");
		}
		else{
			$('#rsvp-submit-btn').attr('disabled', 'true');
			$('#rsvp-submit-btn').addClass("submit-disabled");
		}
    });
	$('#travel-1').on('click', function () {
		if($("select[name='busRoute']").val() != "Please select"){
			$('#rsvp-submit-btn').removeAttr('disabled');
			$('#rsvp-submit-btn').removeClass("submit-disabled");
		}
	});
	$('#travel-2').on('click', function () {
		if($("select[name='busRoute']").val() != "Please select"){
			$('#rsvp-submit-btn').removeAttr('disabled');
			$('#rsvp-submit-btn').removeClass("submit-disabled");
		}
	});
	$("select[name='busRoute']").on('change', function () {
		if($("select[name='busRoute']").val() != ""){
			$('#rsvp-submit-btn').removeAttr('disabled');
			$('#rsvp-submit-btn').removeClass("submit-disabled");
		}
		else{
			$('#rsvp-submit-btn').attr('disabled', 'true');
			$('#rsvp-submit-btn').addClass("submit-disabled");
		}
	});
}

function setupBusRoutes() {
    if ($('#travel-0').is(':checked')){
        $('#bus-routes').removeClass("hidden");
    }
    else {
        $('#bus-routes').addClass("hidden");
    }

    $("input[name='travel']").change(function(){
        if ($('#travel-0').is(':checked')){
            $('#bus-routes').removeClass("hidden");
        }
        else {
            $('#bus-routes').addClass("hidden");
        }
    });
}



function displayRSVP(){
    $('#attend-0').on('click', function () {
			if($('#rsvp-form').css('display') == 'none'){
			$('#rsvp-form').slideDown(function(){
				if($('#rsvp-submit').css('display') == 'none')
				{
					$("#rsvp-submit").slideDown();
				}
				});
			}
			if($('#travel-0').is(':checked') && $("select[name='busRoute']").val() != "Please select"){
				$('#rsvp-submit-btn').removeAttr('disabled');
				$('#rsvp-submit-btn').removeClass("submit-disabled");
			}
			else if($('#travel-1').is(':checked') || $('#travel-2').is(':checked')){
				$('#rsvp-submit-btn').removeAttr('disabled');
				$('#rsvp-submit-btn').removeClass("submit-disabled");
			}
			else{
				$('#rsvp-submit-btn').attr('disabled', 'true');
				$('#rsvp-submit-btn').addClass("submit-disabled");
			}
    });
    $('#attend-1').on('click', function () {
			if($('#rsvp-form').css('display') == 'none' && $('#rsvp-submit').css('display') == 'none'){
				$("#rsvp-submit").slideDown();
			}
			else if($('#rsvp-form').css('display') != 'none'){
				$("#rsvp-form").slideUp();
			}
            $('#rsvp-submit-btn').removeAttr('disabled');
            $('#rsvp-submit-btn').removeClass("submit-disabled");
    });
}


function validateAttendee() {
	return true
}

$(document).ready(function () {
    displayRSVP();
	setupBusRoutes();
	approveBusRoutes();
	
    var form = $('#attendForm');
    $('button#rsvp-submit-btn').click(function (event) {
        event.preventDefault();
        //var stratosphere = $(window).height();
        //stratosphere += 150;
        //stratosphere += 'px';
		
        if (validateAttendee()) {
          //  $(".rocket-ship").animate({
            //    marginBottom: stratosphere
         //   }, {
           //     duration: 2000,
             //   easing: "easeInCirc"
           // });
            //$(".rocket-plume").animate({
           //     opacity: 1,
           //     marginBottom: stratosphere
            //}, {
           //     duration: 2050,
            //    easing: "easeInCirc",
              //  complete: function () {
                    form.submit();
          //      }
				
        } else {
         //   $('.field-missing').show();
         //   $('html, body').animate({
         //       scrollTop: ($('.field-missing').first().offset().top - 30)
         //   }, 500);
        }
    });
	
});