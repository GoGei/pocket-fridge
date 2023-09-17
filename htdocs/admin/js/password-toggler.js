$('.password-toggle').click(function () {
    $(this).toggleClass("fa-eye fa-eye-slash");
    let input = $(this).closest('.form-group').find('input');
    if (input.attr("type") == "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }
});