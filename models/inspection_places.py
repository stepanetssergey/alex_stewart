from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class InspectionPlaces(models.Model):
    
    _name = 'inspection.places'
    
    name = fields.Char(string="Place of inspection")
    address = fields.Char(string="Address of inspection")