(function(){

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


function setupResumePrompt(){
    $('input[name="resume"]').change(function(){
        $('#resume-prompt').toggle();
    });
}

/**
 * Show the more food info field if other is checked, hide if not
 * @param  {boolean} shouldFocus Should the field be focused if it's shown
 */
function updateFoodOtherTextarea(shouldFocus) {
    if ($('input[value="Other"][name="food"]').prop('checked')) {
        $('#foodInfo').slideDown("fast");
        if (shouldFocus) {
            $('#foodInfo').focus();
        }
    } else {
        $('#foodInfo').slideUp("fast");
    }
}

function setupFoodOtherOption() {
    $('input[value="Other"][name="food"]').change(function() {
        updateFoodOtherTextarea(true);
    });

    updateFoodOtherTextarea(false);
}

/**
 * Will autoselect the first name field if nothing is in it (basically if we're on /apply)
 */
function possiblySelectFirstField() {
    var val = $('input[name="nameFirst"]').val();
    if (val === '') {
        $('input[name="nameFirst"]').select();
    }
}

function setupSchoolInputField() {
    var school_data = null;
    $('#school').selectize({
        create: true,
        openOnFocus: true,
        maxItems: 1,
        preload: true,
        'valueField': 'name',
        'labelField': 'name',
        'searchField': ['name'],
        load: function(query, callback) {
            if (school_data !== null) {
                callback(school_data);
                return;
            }

            $.ajax({
                dataType: 'json',
                url: '/apply/schoollist',
                type: 'GET',
                error: function() {
                    console.log("error");
                    school_data = null;
                    callback();
                },
                success: function(res) {
                    school_data = res.schools;
                    callback(res.schools);
                }
            });
        }
    });
}

/**
 * Initialize/setup
 */
$(document).ready(function() {
    setupFoodOtherOption();
    setupResumePrompt();
    possiblySelectFirstField();
    setupSchoolInputField();
});

})();
