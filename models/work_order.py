from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)

#---------------------------------------------------------- model for work order
class WorkOrder(models.Model):
    _name = 'work.order'
    
    name = fields.Char(compute="_get_name")
    Date_of_beginning = fields.Datetime(string='Date of beginning')
    Referance = fields.Char(string='Referance')
    client_work_order = fields.Many2one('res.partner',string='Client')
    material_to_inspect = fields.Many2one('product.template',string='Material')
    services = fields.Many2one('stewart.services',string='Services')
    vessel = fields.Many2one('stewart.vessels',string='Vessel')
    place_of_inspection = fields.Many2one('stewart.places',string='Place of inspection')
    comments = fields.Text(string='Comments')
    responsible = fields.Many2one('res.users',string='Responsible')
    colado_page = fields.Many2one('colado.page',string='Colado Page')
    detail_sheet = fields.Many2one('detail.sheet',string='Detail Sheet')
    user_id = fields.Many2one('res.users',string='Manager')
    
    
    @api.one
    def _get_name(self):
        self.name = 'WO-'+str(self.id)
    
    
    @api.multi
    def send_mail_button(self):
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
            'default_model': 'work.order',
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

        
        
    @api.multi
    def message_get_reply_to(self,res_ids, default=None):
        current_admin = self.env['work.order'].search([])
        return {work_order.id: work_order.client_work_order.id for work_order in current_admin}
     
    @api.multi
    def colado_page_button(self):
        action = self.env.ref('alex_stewart.colado_page_action')
        view_id = self.env.ref('alex_stewart.colado_page_form_view').id
        context = self._context.copy()
        _logger.info(self.name)
        return {
            'name':'work.order',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'colado.page',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':self.colado_page.id,
            'target':action.target,
            'context':context,
        }