from odoo import models, fields, api


class GradeInRejectReasonWizard(models.TransientModel):
    _name = "gradein.reject.reason.wizard"
    _description = "Wizard to select reject reason"

    reject_motive_id = fields.Many2one(
        comodel_name="gradein.reject.reason", string="Motivo de rechazo"
    )

    def save_reject_reason(self):
        # import pdb; pdb.set_trace()
        records = self.env["gradein.order"].browse(self.env.context.get("active_ids"))
        for rec in records:
            rec.write({"state": "rejected", "reject_motive_id": self.reject_motive_id})

        return {"type": "ir.actions.act_window_close"}
