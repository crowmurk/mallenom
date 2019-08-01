$(document).ready(
    function() {
        // Disable form fields autocomplete
        $('#id_full_name').attr('autocomplete', 'off');

        // Auto submit form when fields changed
        $("#id_staff_units").change(function() {
            $(this).parents("form").submit();
        });
    }
);
