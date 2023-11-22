from odoo import models, fields, api


class GradeInRejectReason(models.Model):
    
    _name = 'gradein.reject.reason'
    _description = 'gradein reject reason'
    
    name = fields.Char(string="Nombre")
    active = fields.Boolean(string="activa",default=True)
