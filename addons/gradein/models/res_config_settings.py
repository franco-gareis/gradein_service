from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GradeinConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    equipment_limit_per_month = fields.Integer(
        string="Límite de Equipos por Mes",
        config_parameter="gradein.equipment_limit_per_month",
        default=2
    )

    @api.constrains("equipment_limit_per_month")
    def _check_equipment_limit(self):
        for record in self:
            if record.equipment_limit_per_month < 0:
                raise ValidationError(
                    "El límite de equipos por mes debe ser un número positivo o cero."
                )
            