from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class Customer(models.Model):
    
    _inherit = 'res.partner'
    
    contact_notifications = fields.Many2many('notifications.documents.setting',string="Notifications")
#     attention_of_check = fields.Many2one('res.partner',string="Attention")
#     attention_of = fields.Char()