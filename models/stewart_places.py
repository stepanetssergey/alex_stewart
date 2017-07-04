from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)

class StewartPlaces(models.Model):
    _name = 'stewart.places'
    
    name = fields.Char(string='Name of place')
    address = fields.Char(string='Address')
    comments = fields.Char(string='Description of place')