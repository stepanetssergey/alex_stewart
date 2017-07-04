# -*- coding: utf-8 -*-
import hashlib
import itertools
import logging
import mimetypes
import os
import re
from openerp import models, fields, api
from openerp.tools.translate import _
from pyexcel_xls import get_data
import ast
import json
import base64
import xml.etree.cElementTree as ET
import logging
from openerp.exceptions import UserError, Warning
import urllib
from PIL import Image
from dateutil import relativedelta
import datetime
from dateutil import parser
import StringIO
import logging
_logger = logging.getLogger(__name__)


class ColadoPage(models.Model):
    _name = 'colado.page'
    
    user_id = fields.Many2one('res.users',string='Manager')
    client_colado = fields.Many2one('res.partner',string='Customer')
    name = fields.Char()
    file_name = fields.Char()
    load_file = fields.Many2one('ir.attachment',  string='Hola de colado')
    Reference=fields.Char(string="Reference")
    vessel = fields.Char(string="Vessel")
    port = fields.Char(string="Port")
    cargo = fields.Char(string="Cargo")
    bl_quantity = fields.Float(string="B/L Quantity")
    fore_port_initial = fields.Float(string="Fore Port Initial") 
    fore_port_final = fields.Float(string="Fore Port Final")
    fore_stb_initial = fields.Float(string="Fore Stb Initial")
    fore_stb_final = fields.Float(string="Fore Stb Final")
    aft_port_initial = fields.Float(string="Aft Port Initial")
    aft_port_final = fields.Float(string="Aft Port Final")
    aft_stb_initial = fields.Float(string="Aft Stb Initial")
    aft_stb_final = fields.Float(string="Aft Stb Final")
    mid_port_initial = fields.Float(string="Mid Port Initial")
    mid_port_final = fields.Float(string="Mid Port Final")
    mid_stb_initial = fields.Float(string="Mid Stb Initial")
    mid_stb_final = fields.Float(string="Mid Stb Final")
    keep_correction_initial = fields.Float(string="Keep Correction Initial")
    keep_correction_final = fields.Float(string="Keep Correction Final")
    base_draft_initial = fields.Float(string="Base Draft Initial")
    base_draft_final = fields.Float(string="Base Draft Final")
    base_displa_initial = fields.Float(string="Base Displa Initial")
    base_displa_final = fields.Float(string="Base Displa Final")
    frash_water_initial = fields.Float(string="Frash water Initial")
    frash_water_final = fields.Float(string="Frash water final")
    fuel_oil_initial = fields.Float(string="Fuel Oil Initial")
    fuel_oil_final = fields.Float(string="Fuel Oil Final")
    diesel_oil_initial = fields.Float(string="Diesel Oil Initial")
    diesel_oil_final = fields.Float(string="Diesel Oil Final")
    lub_oil_initial = fields.Float(string="Lub Oil Initial")
    lub_oil_final = fields.Float(string="Lub Oil Final")
    sludge_initial = fields.Float(string="Sludge Initial")
    sludge_final = fields.Float(string="Sludge Final")
    other_initial = fields.Float(string="Other Initial")
    other_final = fields.Float(string="Other Final")
    adv_constant = fields.Float(string="Adv.Constant")
    arrived = fields.Date(string="Arrived")
    pilot_on_board = fields.Date(string="Pilot On Board")
    berthed = fields.Date(string="Berthed")
    commenced = fields.Date(string="Commenced")
    completed = fields.Date(string="Completed")
    fore_dist_initial = fields.Float(string="Fore Dist Initial")
    fore_dist_final = fields.Float(string="Fore Dist Final")
    aft_dist_initial = fields.Float(string="Aft Dist Initial")
    aft_dist_final = fields.Float(string="Aft Dist Final")
    lbp = fields.Float(string="LBP")
    light_ship = fields.Float(string="Light Ship")
    mmt_plus_05_inital = fields.Float(string="Mmt +0.5 Initial")
    mmt_plus_05_final = fields.Float(string="Mmt +0.5 Final")
    mmt_min_05_initial = fields.Float(string="Mmt -0.5 Initial")
    mmt_min_05_final = fields.Float(string="Mmt -0.5 Final")
    density_initial = fields.Float(string="Density Initial")
    density_final = fields.Float(string="Density Final")
    tables_dens_initial = fields.Float(string="Tables Dens Initial")
    tables_dens_final = fields.Float(string="Tables Dens Final")
    
    @api.multi
    def message_get_reply_to(self,res_ids, default=None):
        current_admin = self.env['colado.page'].search([])
        return {colado_page.id: colado_page.client_colado.id for colado_page in current_admin}
    
    @api.multi
    def send_colados_mail_button(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        _logger.info(ir_model_data)
        try:
            template_id = ir_model_data.get_object_reference('alex_stewart', 'email_template_colados')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'colado.page',
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
    
    @api.one
    def _get_name(self):
        self.name = 'Hola de colados'
    
    @api.multi
    def import_colado_button(self):
        file = self.load_file.datas
        colado_data = base64.b64decode(file)
#         _logger.info(colado_data)
        output = StringIO.StringIO()
        output.write(colado_data)
        data = get_data(output)
        test = json.dumps(data, indent=4, sort_keys=True, default=lambda x: str(x))
        test = ast.literal_eval(test)
        _logger.info(test)
        self.Reference = test['Hoja de calados'][1][2]
        self.vessel = test['Hoja de calados'][2][2]
        self.port = test['Hoja de calados'][3][2]
        self.fore_port_initial = test['Hoja de calados'][10][2]
        self.fore_port_final = test['Hoja de calados'][10][3]
        self.bl_quantity = test['Hoja de calados'][5][2]
        self.fore_stb_initial = test['Hoja de calados'][11][2]
        self.fore_stb_final = test['Hoja de calados'][11][3]
        self.aft_port_initial = test['Hoja de calados'][15][2]
        self.aft_port_final = test['Hoja de calados'][15][3]
        self.aft_stb_initial = test['Hoja de calados'][16][2]
        self.aft_stb_final = test['Hoja de calados'][16][3]
        self.mid_port_initial = test['Hoja de calados'][20][2]
        self.mid_port_final = test['Hoja de calados'][20][3]
        self.mid_stb_initial = test['Hoja de calados'][21][2]
        self.mid_stb_final = test['Hoja de calados'][21][3]
        self.keep_correction_initial = test['Hoja de calados'][28][2]
        self.keep_correction_final = test['Hoja de calados'][28][3]
        self.base_draft_initial = test['Hoja de calados'][30][2]
        self.base_draft_final = test['Hoja de calados'][30][3]
        self.base_displa_initial = test['Hoja de calados'][31][2]
        self.base_displa_final = test['Hoja de calados'][31][3]
        self.frash_water_initial = test['Hoja de calados'][38][2]
        self.frash_water_final = test['Hoja de calados'][38][3]
        self.fuel_oil_initial = test['Hoja de calados'][40][2]
        self.fuel_oil_final = test['Hoja de calados'][40][3]
        self.diesel_oil_initial = test['Hoja de calados'][41][2]
        self.diesel_oil_final = test['Hoja de calados'][41][3]
        self.lub_oil_initial = test['Hoja de calados'][42][2]
        self.lub_oil_final = test['Hoja de calados'][42][3]
        self.sludge_initial = test['Hoja de calados'][43][2]
        self.sludge_final = test['Hoja de calados'][43][3]
        self.other_initial = test['Hoja de calados'][44][2]
        self.other_final = test['Hoja de calados'][44][3]
        self.adv_constant = test['Hoja de calados'][50][2]
        self.arrived = test['Hoja de calados'][53][2]
        self.pilot_on_board = test['Hoja de calados'][54][2]
        self.berthed = test['Hoja de calados'][55][2]
        self.commenced = test['Hoja de calados'][56][2]
        self.completed = test['Hoja de calados'][57][2]
        
        
        
        
        
        
    