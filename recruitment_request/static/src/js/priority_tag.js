odoo.define('recruitment_request.PriorityTag', function (require) {
    'use strict';

    const fieldRegistry = require('web.field_registry');
    const FieldChar = require('web.basic_fields').FieldChar;

    const PriorityTag = FieldChar.extend({
        _renderReadonly: function () {
            this._super.apply(this, arguments);
            const value = this.value;
            let colorClass = '';
            if (value === 'low') {
                colorClass = 'tag-low';
            } else if (value === 'medium') {
                colorClass = 'tag-medium';
            } else if (value === 'high') {
                colorClass = 'tag-high';
            }
            this.$el.addClass('priority-tag ' + colorClass);
        },
    });

    fieldRegistry.add('priority_tag', PriorityTag);
});