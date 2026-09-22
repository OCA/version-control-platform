# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VCPRepository(models.Model):
    _inherit = "vcp.repository"

    psc_id = fields.Many2one(
        "vcp.platform.psc",
        readonly=True,
    )
