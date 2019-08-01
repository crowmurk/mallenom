$(document).ready(
    function() {
        // Disable form fields autocomplete
        $("#id_name").attr('autocomplete', 'off');
    }
);

$(document).ready(function() {
    // Add search option to formset selects
    // Disable formset fields autocomplete
    var current_language = $("select[name='language']").val()
    var formset = 'staffing';
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
