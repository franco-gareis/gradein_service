# -*- coding: utf-8 -*-
# from odoo import http


# class Gradein(http.Controller):
#     @http.route('/gradein/gradein', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gradein/gradein/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gradein.listing', {
#             'root': '/gradein/gradein',
#             'objects': http.request.env['gradein.gradein'].search([]),
#         })

#     @http.route('/gradein/gradein/objects/<model("gradein.gradein"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gradein.object', {
#             'object': obj
#         })
