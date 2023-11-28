from datetime import datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class GradeInOrder(models.Model):
    _name = "gradein.order"
    _description = "GradeIn Order"

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Name of the order",
        readonly=True,
        default=lambda self: ("Nueva Orden"),
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

    price = fields.Monetary(
        string="Importe a pagar",
        currency_field="currency_id",
        help="Price that client will pay",
        required=True,
    )

    currency_id = fields.Many2one(related="equipment_id.currency_id")
    question_answer_ids = fields.One2many(
        comodel_name="gradein.question.answer",
        inverse_name="order_id",
        string="Respuestas",
        required=True,
    )
    
    @api.constrains("question_answer_id")
    def validate_answers(self):
        
        for record in self.question_answer_id:
            if record.answer_id.blocking:
                raise ValidationError('Se ha ingresado una respuesta bloqueante, usted no puede continuar con la orden')

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
        if vals_list.get("name", ("Nueva Orden")) == ("Nueva Orden"):
            vals_list["name"] = self.env["ir.sequence"].next_by_code(
                "gradein.order.name"
            ) or ("Nueva Orden")
        res = super().create(vals_list)
        return res

    @api.onchange("equipment_id")
    def on_change_equipment(self):
        """When you select the team you get the questions and answers from the form"""
        lines = [(5, 0, 0)]
        if self.equipment_id:
            for question in self.equipment_id.equipment_type_id.question_ids:
                questions_dict = {"question_id": question.id}
                lines.append((0, 0, questions_dict))
        self.question_answer_ids = lines

    @api.constrains("question_answer_ids")
    def _check_price_not_zero_negative(self):
        """Method validator for records so price is not zero or negative"""
        total = 0
        for question_answer in self.question_answer_ids:
            total += question_answer.answer_id.price_reduction
        if (self.equipment_id.price - total) <= 0:
            raise ValidationError(
                "El importe a pagar no puede ser menor o igual a cero"
            )
        self.price = self.equipment_id.price - total
