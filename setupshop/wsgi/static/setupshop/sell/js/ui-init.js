// IMPORTANT - this file assumes that jQuery has already beeen loaded and document is ready

$(".selectpicker").selectpicker();

// adapted from http://www.abeautifulsite.net/blog/2013/08/whipping-file-inputs-into-shape-with-bootstrap-3/
$(document).on('change', '.btn-file :file', function() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');

        var textinput = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;
        if (textinput.length) {
            textinput.val(log);
        }
        else {
            if (log) alert(log);
        }
});

