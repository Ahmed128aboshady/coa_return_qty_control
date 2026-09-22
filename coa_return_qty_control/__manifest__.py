# -*- coding: utf-8 -*-
{
    'name': 'COA Return Quantity Control',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Block over-returns: prevent returning more than the delivered quantity and display returned vs remaining qty on the return wizard',
    'description': """
COA Return Quantity Control
============================
Prevents users from returning more items than were originally delivered.
Displays real-time "Already Returned" and "Remaining to Return" quantities
directly on the return wizard and the delivery order view.
Eliminates data-entry mistakes and protects inventory accuracy.
Works with all delivery types including partial deliveries and backorders.
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'website': 'https://www.coa-egy.com',
    'support': 'info@coa-egy.com',
    'images': ['static/description/banner.png'],
    'depends': ['stock'],
    'data': [
        'views/stock_return_picking_views.xml',
        'views/stock_picking_views.xml',
    ],
    'price': 49.00,
    'currency': 'USD',
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
}
