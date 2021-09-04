from odoo import fields, models


class DataContent(models.Model):
    _name = "data.content"

    ext_id = fields.Integer()
    name = fields.Char(size=100)
    description = fields.Char(size=128)
    device = fields.Many2one("data.device")
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
            "ext_id",
            "UNIQUE(ext_id)",
            "Multiple devices can't have the same id",
        )
    ]
