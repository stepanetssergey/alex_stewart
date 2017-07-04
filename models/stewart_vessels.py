from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class StewartVessels(models.Model):
    _name = 'stewart.vessels'
    
    name = fields.Char(string='Name of vessels')
    comments = fields.Char(string = 'Description')