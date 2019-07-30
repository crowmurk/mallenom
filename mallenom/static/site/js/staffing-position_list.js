$(document).ready(
    function() {
        // Disable autocompletion on filter form fields
        $('#id_name').attr('autocomplete', 'off');

        // Auto submit filter form when staff units selector changed
        $("#id_staff_units").change(function() {
            $(this).parents("form").submit();
        });
    }
);
