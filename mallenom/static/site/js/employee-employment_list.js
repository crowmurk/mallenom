$(document).ready(
    function() {
        var staff_units = $("#id_staff_units")

        // Disable form fields autocomplete
        $('#id_number').attr('autocomplete', 'off');
        $('#id_employee').attr('autocomplete', 'off');
        $('#id_department').attr('autocomplete', 'off');
        $('#id_position').attr('autocomplete', 'off');

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
