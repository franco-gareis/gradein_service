from datetime import datetime
from odoo import fields, models, api


class GradeInOrder(models.Model):
    _name = "gradein.order"
    _description = "GradeIn Order"

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Name of the order",
        readonly=True,
        default=lambda self: ('New')
    )
    date = fields.Date(default=datetime.today(), required=True)
    state = fields.Selection(
        "_gradein_order_states",
        default="draft",
        string="Estado de la orden",
        required=True,
    )
    equipment_id = fields.Many2one(
        comodel_name="gradein.equipment",
        string="Equipo",
        help="Equipment of the order",
        required=True,
    )
    equipment_type_name = fields.Selection(
        related="equipment_id.equipment_type_id.name"
    )
    image_id = fields.One2many(
        comodel_name="gradein.images",
        inverse_name="order_id",
        string="Imagenes",
        help="Images the of the equipment",
        required=True,
    )
    review = fields.Text(
        string="Resumen de la evaluacion",
        help="Short review of the evaluation",
        required=True,
    )
    reject_motive_id = fields.Many2one(
        comodel_name="gradein.reject.reason", string="Motivo de rechazo"
    )
    imei = fields.Char(string="IMEI", help="IMEI of the equipment to check")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Cliente", required=True
    )
    price = fields.Float(
        string="Importe a pagar", help="Price that client will pay", required=True
    )
    question_answer_id = fields.One2many(
        comodel_name="gradein.question.answer",
        inverse_name="order_id",
        string="Respuestas",
        required=True,
    )


    def _gradein_order_states(self):
        return [
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
            ("paid", "Pagado"),
            ("cancelled", "Cancelado"),
            ("rejected", "Rechazado"),
        ]

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', ('New')) == ('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'gradein.order.name') or ('New')
        res = super().create(vals_list)
        return res