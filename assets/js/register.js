function CheckOther(val){
    var d = document.getElementById('schoolOtherDiv');
    if(val == 'Other')
        d.className = "form-group show";
    else
        d.className = "form-group hidden";
}

function CheckFile(val){
    type = val.files[0].type;
    size = val.files[0].size;
    length = val.files.length;
    var fail = false;
	var error = "Resume <font color=\"red\">";
	if(length < 1)
    {
		fail = true;
        error = error + "<br>Please upload a file";
	}
    if(length > 1)
    {
        fail = true;
        error = error + "<br>Please only upload one file";
	}
    if(type != "application/pdf")
    {
        fail = true;
        error = error + "<br>Resume must be in PDF form";
    }
    if(size >= 2097152)
    {
        fail = true;
        error = error + "<br>Resume must be less than 2 MB";
    }
	error = error + "</font>"
    if(fail)
	{
		var oldFile = document.getElementById("resume");
		var newFile = document.createElement("input");
		newFile.type = "file";
		newFile.id = oldFile.id;
		newFile.name = oldFile.name;
		newFile.accept = oldFile.accept;
		newFile.className = oldFile.className;
		newFile.onchange = oldFile.onchange;
		newFile.required = oldFile.required;
		oldFile.parentNode.replaceChild(newFile, oldFile);
	}
	var oldMessage = document.getElementById("resume_message");
	oldMessage.innerHTML = error;
}

/**
 * Setup the school autofiller
 */
function setupSchoolFiller() {
    $('#email').focusout(function() {
        getSchool();
    });

    if ($('#email').val() != '') {
        getSchool();
    }
}

/**
 * Fetch the school for the value of the email field
 */
function getSchool() {
    $.get('/register/schoolcheck?email=' + $('#email').val(), function(data) {
        if (data === '--') {
            // We don't have a school for the email or something went wrong
            $('#school').attr('disabled', false).val('');
			$('#school').attr('placeholder', "Please enter your school's name");
        }else if (data === '-') {
            // Invalid email format
            $('#school').attr('disabled', true).val('');
			$('#school').attr('placeholder', 'Please enter your email address above.');
        }else {
            // Fill in the school we received from the endpoint
            $('#school').attr('disabled', true).val(data);
        }
    });
}

/**
 * Show/hide a textarea based on the food choice
 */
function setupFoodOtherOption() {
    $('input[name="food"]:radio').change(function() {
        var val = $('input[name="food"]:radio:checked').val();

        if (val === 'Other') {
            $('#foodInfo').show().focus();
        } else {
            $('#foodInfo').hide();
        }
    });
}

/**
 * Select a nonexistent blank item for project-type
 */
function blankProjectType() {
    $('select[name="projectType"]').prop('selectedIndex', -1);
}

/**
 * Initialize/setup
 */
$(document).ready(function() {
    setupSchoolFiller();
    setupFoodOtherOption();
    blankProjectType();
});