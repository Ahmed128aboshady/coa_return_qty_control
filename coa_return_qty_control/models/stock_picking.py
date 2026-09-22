# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_coa_return_summary = fields.Text(
        string="Return Status",
        compute='_compute_x_coa_return_summary',
        help="Per-product summary of delivered / returned / remaining "
             "quantities for this delivery.",
    )

    @api.depends('move_ids.quantity', 'move_ids.state',
                 'move_ids.returned_move_ids.quantity',
                 'move_ids.returned_move_ids.state')
    def _compute_x_coa_return_summary(self):
        for picking in self:
            # Only meaningful for outgoing done deliveries.
            if picking.picking_type_id.code != 'outgoing':
                picking.x_coa_return_summary = False
                continue
            lines = []
            for move in picking.move_ids:
                if move.state != 'done' or move.scrapped:
                    continue
                delivered = move.quantity
                returned = sum(
                    move.returned_move_ids.filtered(
                        lambda m: m.state == 'done' and not m.scrapped
                    ).mapped('quantity')
                )
                remaining = max(delivered - returned, 0.0)
                uom = move.product_id.uom_id.name or ''
                lines.append(
                    "%s: delivered %s, returned %s, remaining %s %s" % (
                        move.product_id.display_name,
                        self._x_coa_fmt(delivered),
                        self._x_coa_fmt(returned),
                        self._x_coa_fmt(remaining),
                        uom,
                    )
                )
            picking.x_coa_return_summary = "\n".join(lines) if lines else False

    @api.model
    def _x_coa_fmt(self, value):
        # Trim trailing zeros for a clean display.
        return ("%g" % value)
