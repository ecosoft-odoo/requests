# © 2017 Ecosoft (ecosoft.co.th).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api

ACTIONS = ("requests.request_request_action_to_review",)


def uninstall_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        for action_id in ACTIONS:
            action = env.ref(action_id)
            action.write(
                {
                    "context": "{}",
                    "domain": "[('approver_ids.user_id','=',uid),"
                    "('state','=','pending')]",
                }
            )
