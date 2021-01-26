odoo.define('requests.Activity', function (require) {
    "use strict";

const field_registry = require('web.field_registry');

require('mail.Activity');

const KanbanActivity = field_registry.get('kanban_activity');

KanbanActivity.include({
    events: Object.assign({}, KanbanActivity.prototype.events, {
        'click .o_activity_action_approve': '_onValidateRequest',
        'click .o_activity_action_refuse': '_onRefuseRequest',
    }),
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * @private
     * @param  {Event} event
     */
    _onValidateRequest(event) {
        const approverID = $(event.currentTarget).data('approver-id');
        this._rpc({
            model: 'request.approver',
            method: 'action_approve',
            args: [[approverID]],
        }).then(result => {
            this.trigger_up('reload', { keepChanges: true });
        });
    },
    /**
     * @private
     * @param  {Event} event
     */
    _onRefuseRequest(event) {
        const approverID = $(event.currentTarget).data('approver-id');
        this._rpc({
            model: 'request.approver',
            method: 'action_refuse',
            args: [[approverID]],
        }).then(result => {
            this.trigger_up('reload', { keepChanges: true });
        });
    },
});

});
