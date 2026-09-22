# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class VCPPlatform(models.Model):
    _inherit = "vcp.platform"

    psc_ids = fields.One2many(
        "vcp.platform.psc",
        inverse_name="platform_id",
        readonly=True,
    )

    def _get_merged_domain(self, start, end, psc_id=None, **values):
        result = super()._get_merged_domain(start, end, psc_id=psc_id, **values)
        if psc_id:
            result.append(("repository_id.psc_id", "=", int(psc_id)))
        return result

    def _get_created_domain(self, start, end, psc_id=None, **values):
        result = super()._get_created_domain(start, end, psc_id=psc_id, **values)
        if psc_id:
            result.append(("repository_id.psc_id", "=", int(psc_id)))
        return result

    def _get_comments_domain(self, start, end, psc_id=None, **values):
        result = super()._get_comments_domain(start, end, psc_id=psc_id, **values)
        if psc_id:
            result.append(("repository_id.psc_id", "=", int(psc_id)))
        return result

    def _get_reviews_domain(self, start, end, psc_id=None, **values):
        result = super()._get_reviews_domain(start, end, psc_id=psc_id, **values)
        if psc_id:
            result.append(("repository_id.psc_id", "=", int(psc_id)))
        return result
