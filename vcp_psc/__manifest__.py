# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Contributors Github Psc",
    "summary": """Integrate PSCs""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": ["vcp_git"],
    "data": [
        "data/vcp_rule.xml",
        "views/vcp_repository.xml",
        "security/ir.model.access.csv",
        "views/vcp_platform_psc.xml",
        "views/vcp_platform.xml",
    ],
    "external_dependencies": {"python": ["PyYAML"]},
    "assets": {},
    "demo": [],
}
