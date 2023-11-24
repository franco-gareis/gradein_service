from odoo import fields, models, api
from odoo.exceptions import ValidationError

class GradeInAnswer(models.Model):
    """Answers for gradein form, 
    if you select "blocking" you 
    cannot continue the form
    Args:
        models (_type_): Model
    """
    _name = "gradein.answer"
    _description = "Answer Model"

    name = fields.Char(required=True, help="Name Answer", string="Nombre")
    price_reduction = fields.Float(string="Reduce el precio en")
    blocking = fields.Boolean(help="Cannot continue with the form", default=False, string="Respuesta bloqueante")
    active = fields.Boolean(help="Activate o desactivate", default=True, string="Activo")
    question_id = fields.Many2one(comodel_name="gradein.question", string="Pregunta", required=True)
    
    @api.constrains('price_reduction')
    def _validate_price_reduction_not_negative(self):
        """Validator method so that the price reduction is not negative"""
        
        for record in self:
            if record.price_reduction < 0:
                raise ValidationError('El precio a reducir no puede ser negativo')

    
