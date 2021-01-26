odoo.define("requests/static/src/models/request/request.js", function (require) {
    "use strict";

    const {registerNewModel} = require("mail/static/src/model/model_core.js");
    const {attr, one2one} = require("mail/static/src/model/model_field.js");

    function factory(dependencies) {
        class Request extends dependencies["mail.model"] {
            // ----------------------------------------------------------------------
            // Public
            // ----------------------------------------------------------------------

            /**
             * Approves the current `request.approver`.
             */
            async approve() {
                await this.async(() =>
                    this.env.services.rpc({
                        model: "request.approver",
                        method: "action_approve",
                        args: [[this.id]],
                    })
                );
                if (this.activity) {
                    this.activity.delete();
                }
                this.delete();
            }

            /**
             * Refuses the current `request.approver`.
             */
            async refuse() {
                await this.async(() =>
                    this.env.services.rpc({
                        model: "request.approver",
                        method: "action_refuse",
                        args: [[this.id]],
                    })
                );
                if (this.activity) {
                    this.activity.delete();
                }
                this.delete();
            }

            // ----------------------------------------------------------------------
            // Private
            // ----------------------------------------------------------------------

            /**
             * @override
             */
            static _createRecordLocalId(data) {
                return `${this.modelName}_${data.id}`;
            }
        }

        Request.fields = {
            activity: one2one("mail.activity", {
                inverse: "request",
            }),
            id: attr(),
            isCurrentPartnerApprover: attr({
                default: false,
                related: "activity.isCurrentPartnerAssignee",
            }),
            status: attr(),
        };

        Request.modelName = "requests.request";

        return Request;
    }

    registerNewModel("requests.request", factory);
});
