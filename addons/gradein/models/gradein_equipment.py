from odoo import fields, models, api
from odoo.exceptions import ValidationError

class GradeInEquipment(models.Model):
    _name = 'gradein.equipment'
    _description = "Equipment Model"
    _rec_name = 'name'

    name = fields.Char(string='Nombre', help='Name of the equipment', required=True)
    active = fields.Boolean(string='Activo', help='If the equipment is active')
    image = fields.Image(string='Imagen', verify_resolution=True, help='Image of the equipment')
    price = fields.Monetary(string='Precio', currency_field='currency_id', help='Price of the equipment')
    description = fields.Text(string='Descripcion', help='Resume of the equipment')
    currency_id = fields.Many2one('res.currency', default=lambda x: x.env.company.currency_id, string='Moneda')

    @api.constrains('price')
    def _check_price_not_zero(self):
        """Method validator for records so price is not zero"""

        if self.price <= float(0):
            raise ValidationError('El precio no puede ser menor o igual a 0')