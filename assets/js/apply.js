function CheckOther(val){
    var d = document.getElementById('schoolOtherDiv');
    if(val == 'Other')
        d.className = "form-group show";
    else
        d.className = "form-group hidden";
}

function CheckFile(val){
    var type = val.files[0].type;
    var size = val.files[0].size;
    var length = val.files.length;
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
	error = error + "</font>";
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
 * Show/hide a textarea based on the food choice
 */
function setupFoodOtherOption() {
    $('input[name="food"]:radio').change(function() {
        var val = $('input[name="food"]:radio:checked').val();

        if (val === 'Other') {
            $('#foodInfo').slideDown("fast").focus();
        } else {
            $('#foodInfo').slideUp("fast");
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
    setupFoodOtherOption();
    blankProjectType();
});

