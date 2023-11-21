import json

from odoo import http
from odoo.http import request, route

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
