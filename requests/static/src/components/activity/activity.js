odoo.define('requests/static/src/components/activity/activity.js', function (require) {
'use strict';

const components = {
    Activity: require('mail/static/src/components/activity/activity.js'),
    Request: require('requests/static/src/components/request/request.js'),
};

Object.assign(components.Activity.components, {
    Request: components.Request,
});

});
