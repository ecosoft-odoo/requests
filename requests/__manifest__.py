# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Requests",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "category": "Human Resources/Requests",
    "website": "https://github.com/OCA/account-payment",
    "license": "AGPL-3",
    "summary": "Create and validate requests",
    "depends": ["mail", "hr", "product"],
    "data": [
        "security/request_security.xml",
        "security/ir.model.access.csv",
        "data/request_category_data.xml",
        "data/mail_activity_data.xml",
        "views/request_template.xml",
        "views/request_category_views.xml",
        "views/request_product_line_views.xml",
        "views/request_request_views.xml",
        "views/res_users_views.xml",
    ],
    "demo": [
        "data/request_demo.xml",
    ],
    "qweb": [
        "static/src/bugfix/bugfix.xml",
        "static/src/components/activity/activity.xml",
        "static/src/components/request/request.xml",
        "static/src/xml/*.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
