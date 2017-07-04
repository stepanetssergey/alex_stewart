from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class NotificationsDocumentsSetting(models.Model):
    
    _name = 'notifications.documents.setting'
    
    
    name = fields.Char(string="Name of document")
    report_id = fields.Many2one('ir.actions.report.xml',string='What Report will be sent')