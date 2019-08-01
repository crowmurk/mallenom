$(document).ready(
    function() {
        // Disable form fields autocomplete
        $('#id_name').attr('autocomplete', 'off');

        // Auto submit form when fields changed
        $("#id_status").change(function() {
            $(this).parents("form").submit();
        });
    }
);
