{
    "name": "GradeIn",
    "version": "1.0",
    "category": "",
    "summary": "",
    "author": ["Ariel Montenegro", "Yamil Ferrufino", "Franco Gareis"],
    "website": "https://www.callefalsa.com.ar",
    "license": "AGPL-3",
    "depends": ["mail"],
    "data": [
        "security/gradein_groups.xml",
        "security/ir.model.access.csv",
        "data/reject_reason.xml",
        "wizard/gradein_reject_reason_wizard.xml",
        "wizard/gradein_confirm_order_wizard.xml",
        "views/res_config_settings.xml",
        "views/services_menu.xml",
        "report/gradein_order_report.xml",
        "views/gradein_equipment_type.xml",
        "views/gradein_equipment.xml",
        "views/gradein_answer.xml",
        "views/gradein_question.xml",
        "views/gradein_reject_reason.xml",
        "views/gradein_order.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "description": """
    """,
}
