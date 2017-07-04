from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class InspectionPrice(models.Model):
    
    _name = 'inspection.price'
    
    price = fields.Float(string='Price')
    description = fields.Char(string='Description')