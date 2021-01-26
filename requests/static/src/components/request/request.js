odoo.define('requests/static/src/components/request/request.js', function (require) {
'use strict';

const useStore = require('mail/static/src/component_hooks/use_store/use_store.js');

const { Component } = owl;

class Request extends Component {

    /**
     * @override
     */
    constructor(...args) {
        super(...args);
        useStore(props => {
            const request = this.env.models['requests.request'].get(props.requestLocalId);
            return {
                request: request ? request.__state : undefined,
            };
        });
    }

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @returns {requests.request}
     */
    get request() {
        return this.env.models['requests.request'].get(this.props.requestLocalId);
    }

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    async _onClickApprove() {
        await this.request.approve();
        this.trigger('o-request-approved');
    }

    /**
     * @private
     */
    async _onClickRefuse() {
        await this.request.refuse();
        this.trigger('o-request-refused');
    }

}

Object.assign(Request, {
    props: {
        requestLocalId: String,
    },
    template: 'requests.Request',
});

return Request;

});
