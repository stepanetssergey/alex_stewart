from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)

class ServicesRequired(models.Model):
    _name = 'services.required'
    
    name = fields.Char(string="Name of Services Required")