from odoo import fields, models


class GradeInOrder(models.Model):
    _name = "gradein.order"
    _description = "GradeIn Order"

    name = fields.Char(required=True, string="Nombre", help="Name of the order")
    date = fields.Date()
    state = fields.Selection(
        [("draft", "Borrador"), ("confirmed", "Confirmado"), ("rejected", "Rechazado")],
        default="draft",
        string="Estado de la orden",
    )
    equipment_id = fields.Many2one(
        comodel_name="gradein.equipment",
        string="Equipo",
        help="Equipment of the order"
    )
    image_id = fields.One2many(
        comodel_name="gradein.images",
        inverse_name="order_id",
        string="Imagenes",
        help="Images the of the equipment",
    )
    review = fields.Text(
        string="Resumen de la evaluacion",
        help="Short review of the evaluation"
    )
    reject_motive_id = fields.Many2one(
        comodel_name="gradein.reject.reason",
        string="Motivo de rechazo"
    )
    imei = fields.Char(string="IMEI", help="IMEI of the equipment to check")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente")
    price = fields.Float(string="Importe a pagar", help="Price that client will pay")
    question_answer_id = fields.One2many(
        comodel_name="gradein.question.answer",
        inverse_name="order_id",
        string="Respuestas"
    )
