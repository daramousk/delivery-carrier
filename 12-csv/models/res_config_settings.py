import os
from ftplib import FTP, FTP_TLS, all_errors
from odoo import api, exceptions, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # html input does not seem to support selecting
    # directories, so for now I will let the user
    # input the *absolute* path to the directory as a string
    # containing the files to be imported
    # (I am not sure if Odoo has implemented a front end widget that does this)
    directory = fields.Char(related="company_id.directory", readonly=False)
    delimiter = fields.Char(
        related="company_id.delimiter",
        readonly=False,
    )
    ftp_host = fields.Char(related="company_id.ftp_host", readonly=False)
    ftps = fields.Boolean(readonly=True)
    ftp_username = fields.Char(
        related="company_id.ftp_username",
        readonly=False,
    )
    ftp_password = fields.Char(
        related="company_id.ftp_password",
        readonly=False,
    )

    @api.onchange("ftp_host")
    def _onchange_ftp_host(self):
        if self.ftp_host and self.ftp_host.startswith("ftps://"):
            self.ftps = True

    @api.constrains("directory")
    def _check_directory(self):
        if not os.path.exists(self.directory):
            raise exceptions.UserError(
                _(
                    "Directory does not exist or is not readable."
                ),
            )

    @api.constrains("ftp_host")
    def _check_ftp_directory(self):
        if self.ftp_host and not self.ftp_host.startswith(
                ("ftp://", "ftps://", )):
            raise exceptions.UserError(
                _(
                    "FTP url must start with either ftp:// or ftps://"),
                )
        else:
            return
        try:
            if self.ftps:
                client = FTP_TLS(
                    self.ftp_host,
                    self.ftp_username,
                    self.ftp_password,
                )
            else:
                client = FTP(
                    self.ftp_host,
                    self.ftp_username,
                    self.ftp_password,
                )
            client.login()
        except all_errors as error:
            raise exceptions.UserError(error)
