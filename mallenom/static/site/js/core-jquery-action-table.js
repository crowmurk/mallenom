// JQuery action-table plugin

(function ($, window, document, undefined) {
    $.fn.actiontable = function() {
        if (this.data.actiontable) {
            return this
        }
        else {
            this.data.actiontable = true;
            return this.each(function() {
                // Find table
                var table = $(this).find('table')
                if (table.length !=1) {
                    console.warn(
                        "Required exacly one table, found:",
                        table.length
                    )
                    return
                }

                // Find table checkboxes
                var headerCheckBox = table.find('thead th :checkbox')
                if (headerCheckBox.length !=1) {
                    console.warn(
                        "Required exacly one checkBox in table header, found:",
                        headerCheckBox.length
                    )
                    return
                }

                var bodyCheckBoxes = table.find('tbody td :checkbox')
                if (!bodyCheckBoxes.length) {
                    console.warn("No row checkboxes found.")
                    return
                }

                // Find button
                var dialog = $(this).find(".action-table-confirm-dialog")
                var form = $(this).find('.action-table-form')
                var button = form.find(':button').not(".action-table-confirm-dialog :button")

                switch (button.length) {
                    case 0:
                        button = undefined
                        break;
                    case 1:
                        bodyCheckBoxes.attr('name', button.attr('value'))
                        // Add confirm dialog
                        button.on("click", function(event) {
                            event.preventDefault();
                            dialog = dialog.dialog({
                                resizable: false,
                                modal: true,
                                appendTo: form
                            });
                            dialog.find('.button-primary').on("click", function(event) {
                                event.preventDefault();
                                dialog.dialog("close");
                            });
                        });
                        break;
                    default:
                        console.warn("Too many buttons found:", button.length)
                        return
                }

                // Set checkboxes click handlers
                headerCheckBox.click(function () {
                    _toggle(this, table, button);
                });
                bodyCheckBoxes.click(function () {
                    _toggle(undefined, table, button);
                });
            })
        }

        function _toggle(source, table, button) {
            var checkboxes = table.find('tbody td :checkbox')

            // Toggle row checkboxes
            if (source !== undefined && checkboxes !== undefined)
                for(var i in checkboxes)
                    checkboxes[i].checked = source.checked;

            // Toggle button
            if (button !== undefined) {
                if (source !== undefined)
                    button.attr("disabled", !source.checked);
                if (checkboxes !== undefined)
                    button.attr("disabled", !checkboxes.is(":checked"));
            }
        }
    }
}(jQuery));
