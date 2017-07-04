from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
import math
_logger = logging.getLogger(__name__)


class StewartStatusScreen(models.Model):
    
    _name = 'stewart.status.screen'
    
    partner_id = fields.Many2one('res.partner',string="Customer")
    sale_order_id = fields.Many2one('sale.order',string="Sale Order")
    status = fields.Many2one('stewart.status.name',string="Status")
    inspector = fields.Many2one('res.users',string="Inspector")
    vessel = fields.Many2one('stewart.vessels',string="Vessel")
    discharge_port = fields.Char()
    b_l_weight = fields.Float(string="B/L Weight")
    current_date = fields.Datetime(string="Current Eta")
    vessel_arrived = fields.Datetime(string="Vessel Arrived")
    p_o_b = fields.Char(string="P.O.B.")
    vessel_berthed = fields.Datetime(string="Vessel Berthed")
    discharge_commenced = fields.Datetime(string="Discharge Commenced")
    discharge_completed = fields.Datetime(string="Discharge Competed")
    list_of_materials = fields.One2many('stewart.list.of.material','status_screen_id',string="List of Materials")
    name = fields.Char(compute="_get_name")
    total_b_l_weight = fields.Float(compute="_total_b_l_weight")
    total_draft_survey_weight = fields.Float(compute="_total_ds_weight")
    total_weightbridge = fields.Float(compute="_total_weightbridge")
#     
    @api.multi
    def _total_weightbridge(self):
        total = 0.0
        for item in self.list_of_materials:
            total = total + float(item.weightbridge)
        self.total_weightbridge = total
        
    @api.multi
    def _total_ds_weight(self):
        total = 0.0
        for item in self.list_of_materials:
            total = total + float(item.draft_survey_weight)
        self.total_draft_survey_weight = total
        
    @api.multi
    def _total_b_l_weight(self):
        total = 0.0
        for item in self.list_of_materials:
            _logger.info(item)
            _logger.info(item.b_l_weight)
            total = total + float(item.b_l_weight)
        self.total_b_l_weight = total
    
    @api.multi
    def send_mail_button_status(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        _logger.info(ir_model_data)
        try:
            template_id = ir_model_data.get_object_reference('alex_stewart', 'email_template_work_order')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'stewart.status.screen',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            #'custom_layout': "sale.mail_template_data_notification_email_sale_order"
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.one
    def _get_name(self):
        self.name = 'Status Screen'
        
    @api.multi
    def message_get_reply_to(self,res_ids, default=None):
        current_admin = self.env['stewart.status.screen'].search([])
        return {stewart_status_screen.id: stewart_status_screen.client_work_order.id for stewart_status_screen in current_admin}
     
class StewartStatusName(models.Model):
    
    _name = 'stewart.status.name' 
    
    name = fields.Char(string="Status")

class StewartListOfMaterial(models.Model):
    
    _name = 'stewart.list.of.material'
    
    status_screen_id = fields.Many2one('stewart.status.screen')
    name = fields.Many2one("material.packing",string="Material")
    b_l_weight = fields.Float(string="B/L Weight")
    draft_survey_weight = fields.Float(string="Draft Survey Weight")
    difference_bl_draft = fields.Float(string="Difference",compute="_difference_bl_draft")
    difference_bl_draft_text = fields.Char(string="Difference",compute="_difference_bl_draft_text")
    weightbridge = fields.Float(string="Weightbridge")
    difference_w = fields.Float(string="Difference",compute="_difference_w")
    difference_w_text = fields.Char(string="Difference",compute="_difference_w_text")
    difference_dws = fields.Float(string="Difference DWS Y WL",compute="_difference_dws")
    difference_dws_text = fields.Char(string="Difference DWS Y WL",compute="_difference_dws_text")
    quality_observed = fields.Char(string="Quality Observed")
    
#     #function for calculation differens fields
    @api.multi
    def _difference_dws_text(self):
        for value in self.search([('id','in',self.ids)]):
            if value.weightbridge !=0:
                value.difference_dws_text = str(math.fabs(round((value.draft_survey_weight-value.weightbridge)/value.weightbridge*100,2)))+' %'
#     
    @api.multi
    def _difference_w_text(self):
        for value in self.search([('id','in',self.ids)]):
            if value.b_l_weight != 0:
                value.difference_w_text = str(math.fabs(round((value.b_l_weight-value.weightbridge)/value.b_l_weight*100,2)))+' %'

    @api.multi
    def _difference_bl_draft_text(self):
        for value in self.search([('id','in',self.ids)]):
            if value.b_l_weight != 0:
                value.difference_bl_draft_text = str(math.fabs(round((value.b_l_weight-value.draft_survey_weight)/value.b_l_weight*100,2)))+' %'
       


  