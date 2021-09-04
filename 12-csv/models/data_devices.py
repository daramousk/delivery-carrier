from odoo import models, fields


class DataDevice(models.Model):
    _name = "data.device"

    ext_id = fields.Integer()
    name = fields.Char(size=32)
    description = fields.Char(size=128)
    code = fields.Char(size=30, index=True)
    expire_date = fields.Datetime()
    state = fields.Selection(
        [
            ("enabled", "Enabled"),
            ("disabled", "Disabled"),
            ("deleted", "Deleted"),
        ],
    )

    _sql_constraints = [
        (
            "code",
            "UNIQUE(code)",
            "Multiple devices can't have the same code",
        ),
        (
            "ext_id",
            "UNIQUE(ext_id)",
            "Multiple devices can't have the same id",
        )
    ]
