function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    xhrFields: {withCredentials: true},
    headers: {'X-CSRFToken': getCookie('csrftoken')},
});

$(document).ready(function () {
    // $('.select2').select2();
});

$('.language-selector').on('click', function (e) {
    e.preventDefault(); // Prevent the default link behavior
    let languageCode = $(this).data('lang');
    $('#select-language input[name="language"]').remove(); // Remove any existing input
    $('#select-language').append($('<input>').attr({
        type: 'hidden',
        name: 'language',
        value: languageCode
    })).submit();
});