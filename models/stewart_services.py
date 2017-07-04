from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class StewartServices(models.Model):
    _name = 'stewart.services'
    
    name = fields.Char(string='Name of service')
    comments = fields.Char(string='Description')
    
    