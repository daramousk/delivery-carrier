import logging
import os
import csv
from ftplib import FTP, FTP_TLS
from odoo import fields, models


logger = logging.getLogger(__name__)


class CsvImport(models.Model):
    _name = "csv.import"

    date = fields.Datetime()
    model = fields.Many2one("ir.model")

    def _import_data_device(self, file):
        logger.debug("Importing device file")
        self.create(
            {
                "date": fields.Datetime.now(),
                "model": self.env["ir.model"].search(
                    [
                        ("model", "=", "data.device"),
                    ],
                ).id,
            },
        )
        device_model = self.env["data.device"]
        for line in csv.reader(
                file,
                delimiter=self.env.user.company_id.delimiter):
            try:
                data = {
                    "ext_id": int(line[0].strip()),
                    "name": line[1].strip(),
                    "description": line[2].strip(),
                    "code": line[3].strip(),
                    # not sure about this date format?
                    # 2017-12-02 23:55:66.333+01:00
                    # "expire_date": line[4].strip(),
                    "state": line[5].strip(),
                }
                record = device_model.search(
                    [("ext_id", "=", line[0])],
                    limit=1,
                )
                if record:
                    record.write(data)
                else:
                    device_model.create(data)
                logger.debug("Device successfully imported {}".format(data))
                self.env.cr.commit()
            except Exception as e:  # TODO be more specific
                self.env.cr.rollback()
                logger.warning("Failed to import device, moving on " + str(e))

    def _import_data_content(self, file):
        logger.debug("Importing data content file")
        self.create(
            {
                "date": fields.Datetime.now(),
                "model": self.env["ir.model"].search(
                    [
                        ("model", "=", "data.device"),
                    ],
                ).id,
            },
        )
        content_model = self.env["data.content"]
        device_model = self.env["data.device"]
        for line in csv.reader(
                file,
                delimiter=self.env.user.company_id.delimiter):
            try:
                dev_id = int(line[3].strip())
                device = device_model.search([("ext_id", "=", dev_id)])
                if not device:
                    device = device_model.create({"ext_id": dev_id})
                data = {
                    "ext_id": int(line[0].strip()),
                    "name": line[1].strip(),
                    "description": line[2].strip(),
                    "device": device.id,
                    # not sure about the date here either
                    # "expire_date": line[4],
                    "state": line[5].strip(),
                }
                content_model.create(data)
                logger.debug("Content successfully imported {}".format(data))
                self.env.cr.commit()
            except Exception as e:  # TODO be more specific here as well
                self.env.cr.rollback()
                logger.warning("Failed to import content, moving on " + str(e))

    def _csv_import(self):
        logger.debug("Starting import")
        if self.env.user.company_id.directory:
            logger.debug(
                "Importing from {}".format(self.env.user.company_id.directory))
            for file_path in os.scandir(self.env.user.company_id.directory):
                file = open(file_path, newline="")
                if file_path.name == "devices.csv":
                    self._import_data_device(file)
                elif file_path.name == "content.csv":
                    self._import_data_content(file)
                else:
                    logger.debug(
                        "Can not import file {}".format(file_path.name))
        if self.env.user.company_id.ftp_host:
            client = FTP_TLS if self.env.user.company_id.ftps else FTP
            with client(
                    self.env.user.company_id.ftp_host,
                    self.env.user.company_id.ftp_username,
                    self.env.user.company_id.ftp_password,
                    ) as client:
                try:
                    from io import StringIO
                    for filename, _ in client.mlsd():
                        if filename == "devices.csv":
                            with StringIO() as file:
                                client.retrbinary(
                                    "RETR " + file,
                                    file.write, 1024)
                                self._import_data_device(file)
                        elif filename == "content.csv":
                            with StringIO() as file:
                                client.retrbinary(
                                    "RETR " + file,
                                    file.write,
                                    1024,
                                )
                                self._import_data_content(file)
                        else:
                            logger.debug(
                                "Importing file {} not supported".format(
                                    filename,
                                )
                            )
                except Exception as e:
                    logger.warning(
                        "FTPS connection failed, error follows: " + e
                    )
