# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
import os
import re

import yaml

from odoo import fields, models

_logger = logging.getLogger(__name__)


class VcpRule(models.Model):
    _inherit = "vcp.rule"

    rule_type = fields.Selection(
        selection_add=[("psc", "PSC Analysis")],
        ondelete={"psc": "cascade"},
    )

    def _process_rule_psc(self, record, parameters=None):
        """
        Process a PSC rule for a given repository.

        :param repository: The repository to process the rule for.
        :param rule: The PSC rule to process.
        """
        if record._name != "vcp.repository.branch":
            # It doesn't make sense to process this kind of rules outside
            # of a repository branch, as they need the code to be downloaded
            # and analyzed.
            return
        record._download_code()
        _logger.info("Downloaded code for repository branch '%s'", record.display_name)
        for conf in self.paths.splitlines():
            conf = conf.strip()
            if not conf or conf.startswith("#"):
                continue
            conf = record.local_path + "/" + conf
            if not os.path.exists(conf):
                _logger.warning(
                    "Path '%s' does not exist for repository branch '%s'",
                    conf,
                    record.display_name,
                )
                continue
            _logger.info(f"Found {conf}")
            for psc_file in os.listdir(os.path.join(record.local_path, conf, "psc")):
                if re.match(r"^.*\.yml$", psc_file):
                    psc_path = os.path.join(record.local_path, conf, "psc", psc_file)
                    with open(psc_path) as f:
                        try:
                            psc_data = yaml.safe_load(f)
                        except yaml.YAMLError as e:
                            _logger.error(f"Error parsing PSC file '{psc_path}': {e}")
                            continue
                    self._process_psc_data(record, psc_data)
            for psc_repo_file in os.listdir(
                os.path.join(record.local_path, conf, "repo")
            ):
                if re.match(r"^.*\.yml$", psc_repo_file):
                    psc_repo_path = os.path.join(
                        record.local_path, conf, "repo", psc_repo_file
                    )
                    with open(psc_repo_path) as f:
                        try:
                            psc_repo_data = yaml.safe_load(f)
                        except yaml.YAMLError as e:
                            _logger.error(
                                f"Error parsing PSC file '{psc_repo_path}': {e}"
                            )
                            continue
                    self._process_psc_repo_data(record, psc_repo_data)

    def _process_psc_data(self, record, psc_data):
        """
        Process the PSC data.

        :param record: The repository branch record to process the PSC data for.
        :param psc_data: The PSC data to process.
        """
        if not psc_data:
            _logger.warning(
                "No PSC data found for repository branch '%s'", record.display_name
            )
            return
        for psc_name in psc_data:
            psc_record = self.env["vcp.platform.psc"].search(
                [
                    ("platform_id", "=", record.platform_id.id),
                    ("key", "=", psc_name),
                ],
                limit=1,
            )
            if not psc_record:
                psc_record = (
                    self.env["vcp.platform.psc"]
                    .sudo()
                    .create(
                        {
                            "platform_id": record.platform_id.id,
                            "key": psc_name,
                            "name": psc_data[psc_name].get("name", psc_name),
                        }
                    )
                )
            else:
                psc_record.sudo().write(
                    {
                        "name": psc_data[psc_name].get("name", psc_name),
                    }
                )
            member_logins = psc_data[psc_name].get("members", []) + psc_data[
                psc_name
            ].get("representatives", [])
            members = []
            for member in member_logins:
                members.append(record.platform_id.host_id._get_user(member))
            psc_record.sudo().member_ids = self.env["vcp.user"].browse(members)

    def _process_psc_repo_data(self, record, psc_repo_data):
        """
        Process the PSC Repository data

        :param record: The repository branch record to process the PSC data for.
        :param psc_repo_data: The PSC Repository data to process.
        """
        if not psc_repo_data:
            _logger.warning(
                "No data found for repository branch '%s'", record.display_name
            )
            return
        for repo_name in psc_repo_data:
            psc_name = psc_repo_data[repo_name].get("psc")
            psc_record = self.env["vcp.platform.psc"].search(
                [
                    ("platform_id", "=", record.platform_id.id),
                    ("key", "=", psc_name),
                ],
                limit=1,
            )
            if not psc_record:
                continue
            repo_record = (
                self.env["vcp.repository"]
                .sudo()
                .search(
                    [
                        ("platform_id", "=", record.platform_id.id),
                        ("name", "=", repo_name),
                    ],
                    limit=1,
                )
            )
            if repo_record:
                repo_record.sudo().write(
                    {
                        "psc_id": psc_record.id,
                    }
                )
