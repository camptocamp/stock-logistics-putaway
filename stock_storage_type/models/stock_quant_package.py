# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    height_in_m = fields.Float(
        help="Technical field, to speed up comparaisons",
        compute="_compute_height_in_m",
        store=True,
    )

    @api.depends("height", "length_uom_id")
    def _compute_height_in_m(self):
        uom_meters = self.env.ref("uom.product_uom_meter")
        for package in self:
            package.height_in_m = package.length_uom_id._compute_quantity(
                qty=package.height,
                to_unit=uom_meters,
                round=False,
            )

    @api.constrains("height", "package_type_id", "product_packaging_id")
    def _check_package_type_height_required(self):
        for package in self:
            if package.package_type_id.height_required and not package.height:
                raise ValidationError(
                    _("The height is mandatory on package {}.").format(package.name)
                )
