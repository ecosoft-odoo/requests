odoo.define('requests/static/src/widgets/form_renderer/form_renderer.js', function (require) {
"use strict";

// ensure `.include()` on `mail` is applied before `requests`
require('mail/static/src/widgets/form_renderer/form_renderer.js');

const FormRenderer = require('web.FormRenderer');


/**
 * Include the FormRenderer to instantiate the chatter area containing (a
 * subset of) the mail widgets (mail_thread, mail_followers and mail_activity).
 */
FormRenderer.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _destroyChatterContainer() {
        this.off('o_request_approved', this);
        this.off('o_request_refused', this);
        this._super(...arguments);
    },
    /**
     * @override
     */
    _makeChatterContainerComponent() {
        this._super(...arguments);
        this.on('o_request_approved', this, ev => this.trigger_up('reload', { keepChanges: true }));
        this.on('o_request_refused', this, ev => this.trigger_up('reload', { keepChanges: true }));
    },
});

});
