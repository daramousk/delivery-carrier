from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    directory = fields.Char()
    delimiter = fields.Char(size=1, default=",")
    ftps = fields.Boolean(readonly=1)
    ftp_host = fields.Char()
    ftp_username = fields.Char(default="anonymous")
    ftp_password = fields.Char(default="anonymous@")
