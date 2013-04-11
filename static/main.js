$(document).ready(function() {
    $(document).on('click', '#regenerate-all', function(e) {
        e.preventDefault();

        $.ajax('/blocks/regenerate/all', {
            type: 'GET',

        }).done(function(data) {
            $('#tracks').html(data);
        });
    });
});
