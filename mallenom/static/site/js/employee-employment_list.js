$(document).ready(
    function() {
        // Disable form fields autocomplete
        $('#id_number').attr('autocomplete', 'off');
        $('#id_employee').attr('autocomplete', 'off');
        $('#id_department').attr('autocomplete', 'off');
        $('#id_position').attr('autocomplete', 'off');

        // Auto submit form when fields changed
        $("#id_staff_units").change(function() {
            $(this).parents("form").submit();
        });
    }
);
