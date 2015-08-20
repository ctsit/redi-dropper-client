$(document).ready(function() {

    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        var icon = $(this).parent().find(".fa")
        if (icon.hasClass('fa-angle-left'))
            icon.removeClass('fa-angle-left').addClass("fa-angle-right");
        else
            icon.removeClass('fa-angle-right').addClass("fa-angle-left");
    });
});
