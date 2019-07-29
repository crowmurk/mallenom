$(document).ready(
    function() {
        // Disable autocompletion on filter form fields
        $('#id_full_name').attr('autocomplete', 'off');

        // Auto submit filter form when count selector changed
        $("#id_staff_units_count").change(function() {
            $(this).parents("form").submit();
        });
    }
);
