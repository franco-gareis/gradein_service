from odoo import fields, models


class GradeInQuestionAnswer(models.Model):
    _name = "gradein.question.answer"
    _description = "Intermediate model of questions and answers"

    question_id = fields.Many2one(
        comodel_name="gradein.question", string="Preguntas", help="Possible questions"
    )
    answer_id = fields.Many2one(
        comodel_name="gradein.answer", string="Respuestas", help="Possible answer"
    )
    order_id = fields.Many2one(comodel_name="gradein.order", ondelete='cascade')
