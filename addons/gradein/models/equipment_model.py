from odoo import fields, models


class EquipmentModel(models.Model):
    _name = 'gradein.equipment'
    _description = "Equipment Model"
    _rec_name = 'name'

    name = fields.Char(string='Nombre', help='Name of the equipment')
    active = fields.Boolean(string='Activo', help='If the equipment is active')
    image = fields.Image(string='Imagen', verify_resolution=True, help='Image of the equipment')
    price = fields.Monetary(string='Precio', currency_field='currency_id', help='Price of the equipment')
    description = fields.Text(string='Descripcion', help='Resume of the equipment')
    currency_id = fields.Many2one('res.currency', default=lambda x: x.env.company.currency_id, string='Moneda')