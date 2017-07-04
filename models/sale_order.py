from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
from docutils.nodes import field
_logger = logging.getLogger(__name__)

class SaleOrderLocation(models.Model):
    _name = 'sale.order.location'
    
    name = fields.Char(string="Location")
    
class MaterialPacking(models.Model):
    _name = 'material.packing'
    
    name = fields.Char(string='Material/Packing')
    
class SaleOrderReportSetting(models.Model):
    _name = 'sale.order.report.setting'
    
    lang = fields.Many2one('res.lang',string="Language")
    quotation_validity = fields.Char(string="Quotation Validity")
    payment_terms = fields.Char(string="Payment Terms")
    advanced_payment_term = fields.Char(string="Advanced Payment Term (where applicable)")
    payment_details = fields.Char(string="Payment Details")
    invoice_currency = fields.Char(string="Invoice Currency")
    taxation = fields.Char(string="Taxation")
    general_terms = fields.Char(string="General Terms")
    detailed_business = fields.Char(string="Detailed T&Cs Business")
    checked_by_audit = fields.Date(string="Checked By, for Audit Purposes")
    general_term_and_conditions = fields.Text(string="General term and conditions")

class SaleOrder(models.Model):
    
    _inherit = 'sale.order'
    
    report_setting = fields.Many2one('sale.order.report.setting')
    work_order = fields.Many2one('stewart.status.screen',string="Status Screen")
    subject = fields.Char(string="Subject")
    services_req = fields.Many2many('services.required',string="Services Required")
    location = fields.Many2one('sale.order.location',string="Location")
    expected_number_of_samples = fields.Integer(string="Inspected # of Samples")
    material_packing = fields.Many2one('material.packing',string='Material/Packing')
    vol_freq_ship_lot = fields.Text(string="Volume, Frequency, Shipment & Lot Size")
    comments = fields.Text(string="Comments")
    comments_analysis = fields.Text(string="Comments Analysis")
    attention_of_check = fields.Many2one('res.partner',string="Attention")
    subject = fields.Text(string="Subject")
    tat = fields.Text(string="Turn Around Time (TAT)")
    internal_comments_inspection = fields.Text(string="Internal Comments Inspection")
    internal_comments_analysis = fields.Text(string="Internal Comments Analysis")
    date_report = fields.Char(compute="_date_format_for_report")
    report_setting = fields.Many2one('sale.order.report.setting')    
    #date for report
    @api.one
    def _date_format_for_report(self):
        month = ['January', 'December', 'March', 'April' ,'May','June','July','August','September','October','November','December']
        date_for_report = self.confirmation_date.split(' ')[0]
        year = date_for_report.split('-')[0]
        month = month[int((date_for_report.split('-')[1]))-1]
        day = date_for_report.split('-')[2]
        date_for_report = day+' '+month+' '+year
        _logger.info(date_for_report)
        self.date_report = date_for_report
    
    #===========================================================================
    # open work_order button
    #===========================================================================
    
    @api.multi
    def work_order_button(self):
        action = self.env.ref('alex_stewart.status_screen_action')
        view_id = self.env.ref('alex_stewart.status_screen_form_view').id
        context = self._context.copy()
        _logger.info(self.name)
        return {
            'name':'stewart.status.screen',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'stewart.status.screen',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':self.work_order.id,
            'target':action.target,
            'context':context,
        }
    
    #============================================================= 
    #      create work order if created sale order
    #=============================================================
    @api.multi
    def _create_work_order(self,values):
        colado_page = self.env['colado.page'].create({'client_colado':values['partner_id']})
        detail_sheet = self.env['detail.sheet'].create({'client_detail':values['partner_id']})
        work_order = self.env['stewart.status.screen'].create({'partner_id':values['partner_id'],
                                                    'inspector':values['user_id'],
                                                     })
        
        return work_order.id
            
    @api.model
    def create(self,values):
        work_order_id = self._create_work_order(values)
        values.update({'work_order':work_order_id})
        res = super(SaleOrder,self).create(values)
        current_status_screen = self.env['stewart.status.screen'].search([('id','=',work_order_id)])
        current_status_screen.write({'sale_order_id':res.id})
        return res