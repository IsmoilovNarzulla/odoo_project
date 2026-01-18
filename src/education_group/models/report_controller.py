from odoo import http
from odoo.addons.web.controllers.report import ReportController

class CustomReportController(ReportController):

    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, **data):
        res = super(CustomReportController, self).report_download(**data)
        return res