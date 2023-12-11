from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GradeinOrderConfirmationWizard(models.TransientModel):
    _name = 'gradein.confirm.order.wizard'
    _description = 'Confirmation Wizard for Gradein Order'

    equipment_id = fields.Many2one('gradein.equipment', string='Equipo', readonly=True)
    price_with_discount = fields.Float(string='Precio con descuento', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True)
    percentage_sum = fields.Float(string='Porcentaje total descontado', readonly=True)
    review = fields.Text(string="Resumen de la evaluación")
    gradein_order_id = fields.Many2one(
        string="Numero de orden",
        comodel_name="gradein.order",
        required=True
    )

    @api.model
    def default_get(self, vals):
        res = super(GradeinOrderConfirmationWizard, self).default_get(vals)
        active_order = self.env['gradein.order'].browse(self._context.get('active_id'))
        res.update(
            {
                "gradein_order_id": active_order.id,
                "equipment_id": active_order.equipment_id.id,
                "partner_id": active_order.partner_id.id,
                "price_with_discount": active_order.total_price_with_discount,
                "percentage_sum": sum(
                    answer.price_reduction_percentage
                    for answer in active_order.question_answer_ids.answer_id
                ),
                "review": active_order.review
            }
        )
        return res

    def action_confirm_order(self):
        """
        Simple action to confirm the order
        """
        for record in self.gradein_order_id.question_answer_ids:
            if not record.answer_id:
                raise ValidationError("Debe ingresar todas las respuestas")

            if record.answer_id.blocking:
                raise ValidationError("Se ha ingresado una respuesta bloqueante, no puede continuar la orden")

        self.gradein_order_id.validate_imei()
        self.gradein_order_id.write(
            {
                "state": "confirmed",
                "review": self.review,
                "price": self.price_with_discount
            }
        )