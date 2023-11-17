from odoo import fields, models

class GradeInEquipmentType(models.Model):
    _name = 'gradein.equipment.type'
    _description = 'Equipment type model'
    _rec_name = 'name'

    name = fields.Char(string='Nombre', required=True, help='Name of the equipment')
    image = fields.Image(string='Imagen', verify_resolution=True, help='Image of the equipment')
    active = fields.Boolean(string='Activo', default=False, help='If the equipment is active')
    question_ids = fields.Many2many(
        comodel_name='gradein.question', string='Preguntas',
        help='Possible question for the equipment',
       
    )