from odoo import models, fields


class GradeInRejectReason(models.Model):
    
    _name = "gradein.reject.reason"
    _description = "gradein reject reason"
    
    name = fields.Char(string="Nombre",required=True)
    active = fields.Boolean(string="Activo",default=True)
