odoo.define('requests/static/tests/helpers/mock_server.js', function (require) {
"use strict";

const MockServer = require('web.MockServer');

MockServer.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    async _performRpc(route, args) {
        if (args.model === 'request.approver' && args.method === 'action_approve') {
            const ids = args.args[0];
            return this._mockRequestApproverActionApprove(ids);
        }
        if (args.model === 'request.approver' && args.method === 'action_refuse') {
            const ids = args.args[0];
            return this._mockRequestApproverActionApprove(ids);
        }
        return this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Private Mocked Methods
    //--------------------------------------------------------------------------

    /**
     * Simulates `action_approve` on `request.approver`.
     *
     * @private
     * @param {integer[]} ids
     */
    _mockRequestApproverActionApprove(ids) {
        // TODO implement this mock and improve related tests (task-2300537)
    },
    /**
     * Simulates `action_refuse` on `request.approver`.
     *
     * @private
     * @param {integer[]} ids
     */
    _mockRequestApproverActionRefuse(ids) {
        // TODO implement this mock and improve related tests (task-2300537)
    },
});

});
