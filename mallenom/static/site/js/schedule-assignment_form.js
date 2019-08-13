$(document).ready(function() {
    // Set employee-employment chained selection
    var employee_field = $("#id_employee")
    var employment_field = $("#id_employment")
    var employment_field_backup = employment_field.html()

    if (employee_field.val() == '') {
        // In create form
        employment_field.attr('disabled', true);
    }
    else {
        // In edit form
        var employment_selected = employment_field.val();
        // Get related employments in JSON
        var url = `/api/employee/${employee_field.val()}/employment`;
        $.getJSON(url, function(employment_json) {
            var employment_valid_pks = employment_json.map(
                (value) => value.pk
            )
            employment_field.html(employment_field_backup)
            employment_field.find('option').filter(function() {
                return this.value && !employment_valid_pks.includes(
                    parseInt(this.value)
                )
            }).remove();
        });
    }

    employee_field.change(function() {
        // Refresh chained selection
        if (employee_field.val() == '') {
            // Disable employment selector when no employee selected
            employment_field.val('');
            employment_field.trigger('change')
            employment_field.attr('disabled', true);
        }
        else {
            var employment_selected = employment_field.val();
            var url = `/api/employee/${employee_field.val()}/employment`;
            $.getJSON(url, function(employment_json) {
                var employment_valid_pks = employment_json.map(
                    (value) => value.pk
                )
                employment_field.html(employment_field_backup)
                employment_field.find('option').filter(function() {
                    return this.value && !employment_valid_pks.includes(
                        parseInt(this.value)
                    )
                }).remove();
                $(employment_field).attr('disabled', false);
            });
        }
    });
});

$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var start_date = $("#id_start")
        var end_date = $("#id_end")

        // Disable form fields autocomplete
        start_date.attr('autocomplete', 'off');
        end_date.attr('autocomplete', 'off');

        // Add datepicker to form date fields
        start_date.datepicker($.extend(
                $.datepicker.regional[current_language]
            ));
        end_date.datepicker($.extend(
            $.datepicker.regional[current_language]
        ));

        // Add search option to form selects
        $("#id_employee").select2({language: current_language})
        $("#id_employment").select2({language: current_language})
    }
);

$(document).ready(function() {
    // Add search option to formset selects
    // Disable formset fields autocomplete
    var current_language = $("select[name='language']").val()
    var formset = 'projectassignments';
    var table = $(`#${formset}_table`);

    // if formset is present
    if (table.length) {
        var selectorsID = `select[id^='id_${formset}-']`;
        var textinputsID = `input[type="text"]input[id^='id_${formset}-']`;
        var selectors = table.find($(selectorsID))
        var textinputs = table.find($(textinputsID))
        var numberOfSelectors = selectors.length;

        // Add search option to selectors
        selectors.select2({language: current_language})
        // Disable autocomplete on text fields
        textinputs.attr('autocomplete', 'off')

        table.bind('DOMSubtreeModified', function() {
            // if new form added in formset
            var newSelectors = table.find($(selectorsID));
            if(newSelectors.length !== numberOfSelectors) {
                numberOfSelectors = newSelectors.length;
                // Add search option to select field in formset
                table.find(
                    $(`select[id^='id_${formset}-${parseInt(numberOfSelectors) - 1}-']`)
                ).select2({language: current_language});
                table.find(
                    $(`input[type="text"]input[id^='id_${formset}-${parseInt(numberOfSelectors) - 1}-']`)
                ).attr('autocomplete', 'off')
            }
        });
    }
});
