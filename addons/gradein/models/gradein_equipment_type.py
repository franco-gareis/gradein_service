from odoo import fields, models


class GradeInEquipmentType(models.Model):
    _name = "gradein.equipment.type"
    _description = "Equipment type model"
    _rec_name = "display_name"

    name = fields.Selection(
        "_equipment_type_selection",
        default="smartphone",
        string="Tipo de equipo",
        help="Name of the equipment",
        required=True
    )
    image = fields.Image(
        string="Imagen",
        verify_resolution=True,
        help="Image of the equipment",
        required=True,
    )
    active = fields.Boolean(
        string="Activo",
        default=True,
        required=True,
        help="If the equipment is active"
    )
    question_ids = fields.Many2many(
        comodel_name="gradein.question",
        string="Preguntas",
        help="Possible question for the equipment",
        required=True,
    )
    equipment_ids = fields.One2many(
        comodel_name="gradein.equipment",
        inverse_name="equipment_type_id",
    )
    display_name = fields.Char(
        store=True,
        compute="_compute_display_name"
    )

    def _equipment_type_selection(self):
        return [
            ("smartphone", "Telefono"),
            ("tv", "Television"),
            ("tablet", "Tablet"),
            ("smartwatch", "SmartWatch")
        ]

    def _compute_display_name(self):
        """Simple method to compute the display_name field"""
        selection = self._equipment_type_selection()

        for sel in selection:
            if sel[0] == self.name:
                self.display_name = sel[1]