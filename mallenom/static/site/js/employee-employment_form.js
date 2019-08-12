$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var employee_field = $("#id_employee")

        // Disable form fields autocomplete
        $("#id_number").attr('autocomplete', 'off');

        // Add search option to form selects
        employee_field.select2({language: current_language});
        employee_field.attr('disabled', 'disabled')
        $("#id_staffing").select2({language: current_language});

        employee_field.closest("form").submit(function() {
            employee_field.removeAttr('disabled');
        });
    }
);
