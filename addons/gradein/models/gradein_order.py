import requests

from requests.exceptions import ConnectionError, HTTPError, ConnectTimeout
from datetime import datetime, timedelta
from odoo import fields, models, api
from odoo.exceptions import ValidationError

REQUEST_ERRORS = (ConnectionError, HTTPError, ConnectTimeout)


class GradeInOrder(models.Model):
    _name = "gradein.order"
    _description = "GradeIn Order"
    _inherit = ["mail.thread", "mail.activity.mixin"]

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
        tracking=True,
    )
    equipment_type_id = fields.Many2one(
        comodel_name="gradein.equipment.type",
        string="Tipo de Equipo",
        help="Equipment Type of the order",
        required=True,
    )
    equipment_id = fields.Many2one(
        comodel_name="gradein.equipment",
        string="Equipo",
        help="Equipment of the order",
        required=True,
    )
    review = fields.Text(
        string="Resumen de la evaluacion",
        help="Short review of the evaluation",
        required=True,
        tracking=True,
    )
    reject_motive_id = fields.Many2one(
        comodel_name="gradein.reject.reason",
        string="Motivo de rechazo",
        tracking=True,
    )
    imei = fields.Char(string="IMEI", help="IMEI of the equipment to check", size=15)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cliente",
        required=True,
        tracking=True,
    )
    price = fields.Monetary(
        string="Importe a pagar",
        currency_field="currency_id",
        help="Price that client will pay",
        required=True,
    )
    currency_id = fields.Many2one(related="equipment_id.currency_id")
    image_ids = fields.Many2many("ir.attachment", string="Imágenes", tracking=True)
    question_answer_ids = fields.One2many(
        comodel_name="gradein.question.answer",
        inverse_name="order_id",
        string="Respuestas",
        required=True,
        tracking=True,
    )
    equipment_type_name = fields.Selection(related="equipment_type_id.name")

    def _gradein_order_states(self):
        return [
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
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

    @api.onchange("equipment_type_id")
    def get_questions_by_equipment_type(self):
        """When you select the equipment you get the questions and answers from the form"""
        commands_data = [(5, 0, 0)]  # We delete all the questions first
        if self.equipment_type_id:
            for question in self.equipment_type_id.question_ids:
                questions_dict = {"question_id": question.id}
                commands_data.append(
                    (0, 0, questions_dict)
                )  # We create this records with the questions of the equipment
        self.question_answer_ids = commands_data

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

    @api.constrains("partner_id")
    def validate_order_user(self):
        """
        Checks the number of orders the customer had in a month

        Raises:
            ValidationError: If the customer has exceeded the order limit
        """

        ORDER_LIMIT_DAYS = 30

        max_orders = int(self.env["ir.config_parameter"].sudo().get_param("max_orders"))
        monthly_user_orders = datetime.today() - timedelta(days=ORDER_LIMIT_DAYS)

        for record in self:
            numbers_of_records = self.env["gradein.order"].search_count(
                [
                    ("partner_id", "=", record.partner_id.id),
                    ("state", "=", "confirmed"),
                    ("date", ">", monthly_user_orders),
                    ("date", "<=", datetime.today()),
                ]
            )

            if numbers_of_records >= max_orders:
                raise ValidationError(
                    f"El usuario ha superado el limite de {max_orders} ordenes permitidos en un periodo de {ORDER_LIMIT_DAYS} días"
                )

    @api.constrains("imei")
    def validate_imei(self):
        if self.equipment_type_name == "smartphone":
            url = f"https://mirgor-alkemy-imei-api.azurewebsites.net/api/check_imei/{self.imei}"

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

            except REQUEST_ERRORS as err:
                raise ValidationError(
                    f"Ocurrio un error inesperado: {err}"
                )

            response_json = response.json()
            is_valid_imei = response_json.get("valid")

            if not is_valid_imei:
                raise ValidationError(
                    "El imei no es valido para realizar esta operacion"
                )
            else:
                notification = {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": ("Validador de IMEI"),
                        "message": "El IMEI ingresado es valido",
                        "type": "success",
                        "sticky": True,
                    },
                }

            return notification

    def action_confirm_order(self):
        """
        Simple action to confirm the order

        Returns:
            None
        """
        for record in self.question_answer_ids:
            if record.answer_id.blocking:
                raise ValidationError(
                    "Se ha ingresado una respuesta bloqueante, usted no puede continuar con la orden"
                )
        self.write({"state": "confirmed"})

    def action_draft_order(self):
        """Simple action to draft the order"""
        self.write({"state": "draft"})
