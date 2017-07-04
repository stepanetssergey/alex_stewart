# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.website_portal.controllers.main import website_account


class website_account(website_account):

    @http.route()
    def account(self, **kw):
        """ Add sales documents to main account page """
        response = super(website_account, self).account(**kw)
        partner = request.env.user.partner_id

        StatusScreen = request.env['stewart.status.screen']
        status_screen_count = StatusScreen.search_count([
            ('partner_id', 'in', [partner.commercial_partner_id.id])
        ])

        response.qcontext.update({
            'status_screen_count': status_screen_count,
        })
        return response
    
    @http.route(['/my/screen/<int:screen>'], type='http', auth="user", website=True)
    def status_screen_followup(self, screen, **kw):
        screen = request.env['stewart.status.screen'].browse([screen])
#             try:
#                 screen.check_access_rights('read')
#                 screen.check_access_rule('read')
#             except AccessError:
#                 return request.render("website.403")

        screen_sudo = screen.sudo()
        screen_lines = {il.name.id: il.id for il in screen_sudo.mapped('list_of_materials')}

        return request.render("alex_stewart.status_screen_followup", {
            'screen': screen_sudo,
            'screen_lines': screen_lines,
        })
        
    @http.route(['/my/status_screens', '/my/status_screens/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_status(self, page=1, date_begin=None, date_end=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        StatusScreen = request.env['stewart.status.screen']

        domain = [
            ('partner_id', 'in', [partner.commercial_partner_id.id])
        ]
        archive_groups = self._get_archive_groups('stewart.status.screen', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        status_count = StatusScreen.search_count(domain)
        # pager
        pager = request.website.pager(
            url="/my/status_screens",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=status_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        statuses = StatusScreen.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'statuses': statuses,
            'page_name': 'Screen',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/status_screens',
        })
        return request.render("alex_stewart.portal_my_status_screens", values)

#    
    