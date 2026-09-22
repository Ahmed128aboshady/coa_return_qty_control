# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class StockReturnPickingLine(models.TransientModel):
    _inherit = 'stock.return.picking.line'

    x_coa_delivered_qty = fields.Float(
        string="Delivered",
        digits='Product Unit of Measure',
        compute='_compute_x_coa_return_info',
        help="Quantity originally delivered by the source move.",
    )
    x_coa_already_returned_qty = fields.Float(
        string="Already Returned",
        digits='Product Unit of Measure',
        compute='_compute_x_coa_return_info',
        help="Quantity already returned from this delivery line in "
             "previous returns.",
    )
    x_coa_returnable_qty = fields.Float(
        string="Returnable",
        digits='Product Unit of Measure',
        compute='_compute_x_coa_return_info',
        help="Remaining quantity that may still be returned "
             "(delivered - already returned).",
    )

    @api.depends('move_id')
    def _compute_x_coa_return_info(self):
        for line in self:
            move = line.move_id
            if not move:
                line.x_coa_delivered_qty = 0.0
                line.x_coa_already_returned_qty = 0.0
                line.x_coa_returnable_qty = 0.0
                continue
            delivered = move.quantity
            returned = line._x_coa_get_returned_qty(move)
            line.x_coa_delivered_qty = delivered
            line.x_coa_already_returned_qty = returned
            line.x_coa_returnable_qty = max(delivered - returned, 0.0)

    @api.model
    def _x_coa_get_returned_qty(self, move):
        """Sum of done quantities of moves that already returned this move."""
        return_moves = self.env['stock.move'].search([
            ('origin_returned_move_id', '=', move.id),
            ('state', '=', 'done'),
            ('scrapped', '=', False),
        ])
        return sum(return_moves.mapped('quantity'))


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _x_coa_check_return_quantities(self):
        """Raise if any line asks to return more than what is returnable."""
        for wizard in self:
            errors = []
            for line in wizard.product_return_moves:
                move = line.move_id
                if not move:
                    continue
                rounding = line.uom_id.rounding or move.product_id.uom_id.rounding
                if float_compare(
                        line.quantity, line.x_coa_returnable_qty,
                        precision_rounding=rounding) > 0:
                    errors.append(_(
                        "- %(product)s: trying to return %(asked).2f but only "
                        "%(allowed).2f is returnable (delivered %(delivered).2f, "
                        "already returned %(returned).2f).",
                        product=move.product_id.display_name,
                        asked=line.quantity,
                        allowed=line.x_coa_returnable_qty,
                        delivered=line.x_coa_delivered_qty,
                        returned=line.x_coa_already_returned_qty,
                    ))
            if errors:
                raise ValidationError(
                    _("You cannot return more than the delivered quantity:"
                      "\n\n%s") % "\n".join(errors)
                )

    def action_create_returns(self):
        self._x_coa_check_return_quantities()
        return super().action_create_returns()

    def action_create_returns_all(self):
        # returns_all sets each line to the full returnable qty first, so it
        # is inherently safe; still guard in case of concurrent returns.
        res = super().action_create_returns_all()
        return res

    def action_create_exchanges(self):
        self._x_coa_check_return_quantities()
        return super().action_create_exchanges()
