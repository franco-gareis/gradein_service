import json

from odoo import http
from odoo.http import request, route
from odoo.exceptions import MissingError


HEADERS = [("Content-Type", "application/json"), ("Cache-Control", "no-store")]


class GradeInController(http.Controller):

    def _process_questions(self, recordset):        
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
    def get_gradein_questions(self, **kwargs):
        """_summary_

        Returns:
            _type_: _description_
        """
        recordset = request.env["gradein.equipment.type"].sudo().search([])
        equipment_type_id = kwargs.get("equipment_type_id")
            
        if equipment_type_id and recordset:
            recordset = recordset.browse([int(equipment_type_id)])
            
        try:
            data = self._process_questions(recordset)
        except MissingError:
            return request.not_found()
        
        return request.make_response(data, headers=HEADERS)
        
