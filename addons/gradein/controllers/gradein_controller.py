import json

from odoo import http
from odoo.http import request, route
from odoo.exceptions import MissingError


HEADERS = [("Content-Type", "application/json"), ("Cache-Control", "no-store")]


class GradeInController(http.Controller):
    def _process_data_by_equipment_id(self, recordset):
        data = json.dumps(
            {
                "equipment_type_id": recordset.id,
                "equipment_type_name": recordset.name,
                "questions": [
                    {question.name: question.answer_ids.mapped("name")}
                    for question in recordset.question_ids
                ],
            }
        )
        return data

    def _process_all_questions(self, recordset):
        data = json.dumps(
            [
                {
                    "equipment_type_id": eq.id,
                    "equipment_type_name": eq.name,
                    "questions": [
                        {question.name: question.answer_ids.mapped("name")}
                        for question in eq.question_ids
                    ],
                }
                for eq in recordset
            ]
        )
        return data

    @route("/gradein/questions/", type="http", auth="public", methods=["GET"])
    def get_gradein_questions(self):

        equipment_type_id = request.params.get("equipment_type_id")

        try:
            if equipment_type_id:
                recordset = (
                    request.env["gradein.equipment.type"]
                    .sudo()
                    .browse([int(equipment_type_id)])
                )
                data = self._process_data_by_equipment_id(recordset)
            else:
                recordset = request.env["gradein.equipment.type"].sudo().search([])
                data = self._process_all_questions(recordset)

            return request.make_response(data, headers=HEADERS)
        except MissingError:
            return request.not_found()
    
    
    @route("/gradein/questions/", auth="api_key", type='http', methods=["GET"])
    
    def get_gradein_answer(self): 
        answers = request.env["gradein.answer"].sudo().search([])
        
        answers_list = []
        for answer in answers:
            answers_list.append({
                "name": answer.name,
                "price_reduction": answer.price_reduction,
                "blocking": answer.blocking,
            })
                
        data = json.dumps(answers_list)
        return request.make_response(data, headers=HEADERS)
        
        # 5e71a3b7ae439318fb49d143de3d1e1f867e2fc9
