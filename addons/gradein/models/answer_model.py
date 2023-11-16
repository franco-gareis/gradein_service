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

    name = fields.Char(required=True, help="Name Answer", string="Name")
    currency = fields.Many2one("res.currency", string="Currency")
    price_reduction = fields.Monetary(string="Price Reduction", currency_field="currency")
    blocking = fields.Boolean(help="Cannot continue with the form", default=False)
    activo = fields.Boolean(help="Activate o desactivate", required=True, default=True)
