from openerp import models, fields, api
from openerp.tools.translate import _
import xml.etree.cElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class DetailSheet(models.Model):
    _name = 'detail.sheet'
    
    name = fields.Char(string="Name of detail sheet")
    materials = fields.One2many('materials','detail_sheet_id',string="Materials")
    client_detail = fields.Many2one('res.partner',string='Customer')

class Materials(models.Model):
    _name = 'materials'
    
    detail_sheet_id = fields.Integer(string="Id of list sheet")
    material_name = fields.Char(string="Material name")
    cantidad_bl = fields.Char(string="Candidad BL")
    cantidad_bl_name = fields.Char()
    materials_line = fields.One2many('materials.name','materials_id',string="Materials Analysis")
    
class MaterialsLine(models.Model):
    
    _name = 'materials.name'
    
    materials_id = fields.Integer(string="Id of materials")
    sequence_id = fields.Integer(string="Number")
    fecha = fields.Date(string="Fecha")
    hora = fields.Float(string="Hora")
    matricula = fields.Char(string="Matricula")
    bruto = fields.Float(string="Bruto")
    tara = fields.Float(string="Tara")
    neto = fields.Float(string="Neto")
    