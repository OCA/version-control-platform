# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VCPUser(models.Model):
    _inherit = "vcp.user"

    psc_ids = fields.Many2many(
        comodel_name="vcp.platform.psc",
        readonly=True,
    )
