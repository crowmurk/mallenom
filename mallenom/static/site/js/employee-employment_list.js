$(document).ready(
    function() {
        // Disable autocompletion on filter form fields
        $('#id_number').attr('autocomplete', 'off');
        $('#id_employee').attr('autocomplete', 'off');
        $('#id_department').attr('autocomplete', 'off');
        $('#id_position').attr('autocomplete', 'off');

        // Auto submit filter form when staff units selector changed
        $("#id_staff_units").change(function() {
            $(this).parents("form").submit();
        });
    }
);
