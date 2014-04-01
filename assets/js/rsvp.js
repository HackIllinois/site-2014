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
	if($("input[name='attend']:checked").val() == "Yes"){
		if($("input[name='travel']:checked").val() == 'I will provide my own transportation' || $("input[name='travel']:checked").val() == 'I am already in Urbana-Champaign, IL'){
		    return "valid";
		}
		else if($("input[name='travel']:checked").val() == 'I would like to ride a HackIllinois bus' && $("[name='busRoute']").val() == ""){
			return "Please chose a Bus Route";
		}
		else if($("input[name='travel']:checked").val() == 'I would like to ride a HackIllinois bus' && $("[name='busRoute']").val() != ""){
			return "valid";
		}
		else if($("input[name='travel']:checked").val() == ""){
			return "Please chose a travel Arragnement";
		}
		else{
			return "There was an unforeseen error please try again";
		}
	}
	else if($("input[name='attend']:checked").val() == "No"){
		return "valid";
	}
}

$(document).ready(function () {
    displayRSVP();
	setupBusRoutes();
	approveBusRoutes();
	
	if($("[name='attend']:checked").val() == "Yes"){
		$('#attend-0').click();
	}
    var form = $('#attendForm');
    $('button#rsvp-submit-btn').click(function() {
		validation = validateAttendee();
        if (validation == "valid") {
            form.submit();
        } 
		else {
            $('.field-missing').show();
			$('.errormessages').text(validation);
            $('html, body').animate({scrollTop: ($('.field-missing').first().offset().top - 30)}, 500);
        }
    });
	
});