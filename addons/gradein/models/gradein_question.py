# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GradeInQuestion(models.Model):
    
    _name = 'gradein.question'
    _description = 'gradein questions'
    
    name = fields.Char(string="Nombre",required=True)
    active = fields.Boolean(string="activa",default=True)
    equipment_type_ids = fields.Many2many(comodel_name="gradein.equipment.type",string="Tipos de equipo",required=True)
    answer_ids = fields.One2many(comodel_name="gradein.answer",string="Respuestas posibles", inverse_name="question_id",required=True)
    

