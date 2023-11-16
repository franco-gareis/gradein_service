# -*- coding: utf-8 -*-
from odoo import models, fields, api


class QuestionModel (models.Model):
    
    _name = 'gradein.question'
    _description = 'gradein questions'
    
    name = fields.Char(string="Nombre")
    active = fields.Boolean(string="activa")
    equipment_type_ids = fields.Many2one(comodel_name="gradein.equipment_types",string="Tipos de equipo")
    answer_ids = fields.One2many(comodel_name="gradein.answer",string="Respuestas posibles")
    

