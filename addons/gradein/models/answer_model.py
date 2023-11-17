from odoo import fields, models


class AnswerModel(models.Model):
    """Questions for gradein form, 
    if you select "blocking" you 
    cannot continue the form
    Args:
        models (_type_): Model
    """
    _name = "gradein.answer"
    _description = "Answer Model"

    name = fields.Char(required=True, help="Name Answer", string="Nombre")
    currency = fields.Many2one("res.currency", string="Moneda")
    price_reduction = fields.Monetary(string="Reduce el precio en", currency_field="currency")
    blocking = fields.Boolean(help="Cannot continue with the form", default=False, string="Respuesta bloqueante")
    activo = fields.Boolean(help="Activate o desactivate", default=True)
    question_id = fields.Many2one(comodel_name="gradein.question", inverse_name="answer_ids")
    