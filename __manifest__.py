{
    'name': "Alex Steward",
    'version': '1.0',
    'depends': ['base',
                'sale',
                'sales_team',
                'delivery',
                'barcodes',
                'mail',
                'report',
                'portal_sale',
                'website_portal',
                'website_payment',],
    'author': "Sergey Stepanets",
    'category': 'Application',
    'description': """
    Module that realize workflow of Alex Steward corporation
    """,
    'data': [
      'views/stewart_vessels.xml',
      'views/stewart_services.xml',
      'views/inspection_places.xml',
      #'views/work_order.xml',
      'views/sale_order.xml',
      'views/colado_page.xml',
      'views/detail_sheet.xml',
      'views/notifications_setting.xml',
      'views/customers.xml',
      'views/services_required.xml',
      'reports/cert_analysis_report.xml',
      'reports/peso_por_colados.xml',
      'data/mail_work_order_template.xml',
      'data/mail_colado_template.xml',
      'views/locations.xml',
      'views/material_packing.xml',
    'views/status_screen.xml',
    'views/sale_order_setting.xml',
    'views/portal/website_portal_status_screen_templates.xml',

#     'views/report.xml',
    ],
}