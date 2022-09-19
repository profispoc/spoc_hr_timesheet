odoo.define('spoc_hr_timesheet.suggested_recipient_info', function (require) {
    'use strict';

    const { registerFieldPatchModel, } = require('@mail/model/model_core');
    const { attr, } = require('@mail/model/model_field');

    registerFieldPatchModel('mail.suggested_recipient_info', 'spoc_hr_timesheet.suggested_recipient_info', {

        isSelected: attr({
            compute: '_computeIsSelected',
            default: false,
        }),

    });

});
