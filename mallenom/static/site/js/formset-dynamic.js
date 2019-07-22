$(document).ready(function() {
    $('#formset_add_form_button').click(function() {
        // Add new forms in formset
        var options = $(this).data();

        if (options !== undefined) {
            var form_idx = $(`#id_${options.prefix}-TOTAL_FORMS`).val();
            $(`#${options.formset}`).append($(`#${options.form}`).html().replace(/__prefix__/g, form_idx));
            $(`#id_${options.prefix}-TOTAL_FORMS`).val(parseInt(form_idx) + 1);
        }
    });
});
