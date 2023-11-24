from odoo import fields, models


class GradeInImages(models.Model):
    _name = "gradein.images"
    _description = "Simple model to save all the images from the order"

    image = fields.Image(
        string='Imagen',
        verify_resolution=True,
        help="Image from the equipment"
    )