import json

from odoo import http
from odoo.http import request, route
import xmlrpc.client

HEADERS = [("Content-Type", "application/json"), ("Cache-Control", "no-store")]


class GradeInController(http.Controller):

    @route(
        "/gradein/questions/equipment-type-id/<int:equipment_type_id>",
        type="http",
        auth="public",
        methods=["GET"],
    )
    def get_gradein_questions(self, equipment_type_id):
        equipment = request.env["gradein.equipment.type"].sudo().browse([equipment_type_id])

        if equipment.exists():
            data = json.dumps(
                {
                    "equipment_type_id": equipment.id,
                    "equipment_type_name": equipment.name,
                    "questions": [
                        {question.name: question.answer_ids.mapped("name")}
                        for question in equipment.question_ids
                    ],
                }
            )

            return request.make_response(data, headers=HEADERS)
        else:
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
