$( document ).ready(function() {
    $('#other-food-click').on('click', function(){
        $("#other-food-specify").slideDown("fast");
        $("#other-food-specify").attr("required", true);
    });

});

