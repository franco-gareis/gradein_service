from odoo import models, fields, api


class GradeInRejectReasonWizard(models.TransientModel):
    _name = "gradein.reject.reason.wizard"
    _description = "Wizard to select reject reason"

    review = fields.Text(string="Resumen de la evaluación")
    reject_motive_id = fields.Many2one(
        comodel_name="gradein.reject.reason",
        string="Motivo de rechazo"
    )

    @api.model
    def default_get(self, vals):
        res = super(GradeInRejectReasonWizard, self).default_get(vals)
        active_order = self.env["gradein.order"].browse(self._context.get("active_id"))
        res.update({"review": active_order.review})
        return res

    def save_reject_reason(self):
        active_order = self.env["gradein.order"].browse(self._context.get("active_id"))
        active_order.write(
            {
                "state": "rejected",
                "reject_motive_id": self.reject_motive_id,
                "review": self.review,
            }
        )

        return {"type": "ir.actions.act_window_close"}
