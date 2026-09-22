# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VCPPlatformPsc(models.Model):
    _name = "vcp.platform.psc"
    _description = "Version Control Platform PSC"

    platform_id = fields.Many2one(
        comodel_name="vcp.platform",
        string="Platform",
        required=True,
    )
    name = fields.Char(required=True)
    key = fields.Char(required=True)
    member_ids = fields.Many2many(
        "vcp.user",
        readonly=True,
    )
