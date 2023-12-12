from odoo import fields, models, api
from odoo.exceptions import ValidationError


class GradeInEquipment(models.Model):
    _name = "gradein.equipment"
    _description = "Equipment Model"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Nombre", help="Name of the equipment", required=True, tracking=True
    )
    active = fields.Boolean(
        string="Activo",
        required=True,
        default=True,
        help="If the equipment is active",
        tracking=True,
    )
    image = fields.Image(
        string="Imagen",
        verify_resolution=True,
        help="Image of the equipment",
        tracking=True,
    )
    price = fields.Monetary(
        string="Precio",
        currency_field="currency_id",
        help="Price of the equipment",
        required=True,
        tracking=True,
    )
    equipment_type_id = fields.Many2one(
        comodel_name="gradein.equipment.type",
        string="Tipo de equipo",
        help="Wich type is the equipment",
        tracking=True,
    )
    description = fields.Text(string="Descripcion", help="Resume of the equipment")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda x: x.env.company.currency_id,
        string="Moneda",
        required=True,
        tracking=True,
    )

    @api.constrains("price")
    def _check_price_not_zero(self):
        """Method validator for records so price is not zero"""

        for record in self:
            if record.price <= 0:
                raise ValidationError("El precio no puede ser menor o igual a 0")
