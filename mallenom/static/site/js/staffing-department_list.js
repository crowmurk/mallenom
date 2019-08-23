$(document).ready(
    function() {
        var staff_units = $("#id_staff_units")

        // Disable form fields autocomplete
        $('#id_name').attr('autocomplete', 'off');

        // Add search option to form selects
        staff_units.select2({
            minimumResultsForSearch: Infinity,
            width: '50pt',
        })

        // Auto submit form when fields changed
        staff_units.change(function() {
            $(this).parents("form").submit();
        });
    }
);
