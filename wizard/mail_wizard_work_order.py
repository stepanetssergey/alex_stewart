# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        if self._context.get('default_model') == 'stewart.status.screen' and self._context.get('default_res_id'):
            order = self.env['stewart.status.screen'].browse([self._context['default_res_id']])
            self = self.with_context(mail_post_autofollow=False)
        return super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
