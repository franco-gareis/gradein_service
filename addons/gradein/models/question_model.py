# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Question (models.Model):
    
    _name = 'question.model'
    _description = 'gradein.questions'
    
    name = fields.Char()
    active = fields.Boolean()
    equipment_type_ids = fields.Many2one(comodel_name ="tabla_equipments",string="equipment")
    answer_ids = fields.One2many(comodel_name="tabla_answer",string="answers")
    

