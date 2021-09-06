from odoo import api, fields, models, _

import logging

_logger = logging.getLogger()


class SocialPushWizard(models.TransientModel):
    _name = "social.push.wizard"
    _description = "social.push.wizard"

    post_id = fields.Many2one('social.post')

    def action_do(self):
        """
        send the post to the visitors from the context
        :return: action
        """
        visitor_ids = self.env.context.get("active_id", False)
        _logger.info("action_do: visitor_ids %s", visitor_ids)
        res = {
            'name': _('Send Post to Visitors'),
            'type': 'ir.actions.act_window',
            'res_model': 'social.post',
            # 'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': '{}',
        }
        if bool(visitor_ids):
            visitors = self.env["website.visitor"].browse(visitor_ids)
            # if all(visitor.push_token for visitor in self):
            push_media = self.env['social.media'].search([('media_type', '=', 'push_notifications')])
            post_id = self.post_id.copy()
            post_id.account_ids = push_media.account_ids.ids
            post_id.visitor_domain = "[('push_token', '!=', False), ('id', 'in', %s)]" % self.ids
            res.update({"res_id": post_id.id})

        return res
