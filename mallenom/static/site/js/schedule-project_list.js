$(document).ready(
    function() {
        var status = $("#id_status")

        // Disable form fields autocomplete
        $('#id_name').attr('autocomplete', 'off');

        // Add search option to form selects
        status.select2({
            minimumResultsForSearch: Infinity,
            width: '50pt',
        })

        // Auto submit form when fields changed
        status.change(function() {
            $(this).parents("form").submit();
        });
    }
);
