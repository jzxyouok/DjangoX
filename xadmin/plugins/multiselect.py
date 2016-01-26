#coding:utf-8

import xadmin
from django.db.models import ManyToManyField

from xadmin.views import BaseAdminPlugin, ModelFormAdminView
from xadmin import widgets

class M2MSelectPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'style_fields') and \
            (
                'm2m_transfer' in self.admin_view.style_fields.values() or
                'm2m_dropdown' in self.admin_view.style_fields.values() or
                
                'm2m_raw' in self.admin_view.style_fields.values() or
                'm2m_ajax' in self.admin_view.style_fields.values() or
                'm2m_ajax_multi' in self.admin_view.style_fields.values() or
                'm2m_select2' in self.admin_view.style_fields.values()
            )

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'm2m_transfer' and isinstance(db_field, ManyToManyField):
            return {'widget': widgets.SelectMultipleTransfer(db_field.verbose_name, False), 'help_text': ''}
        if style == 'm2m_dropdown' and isinstance(db_field, ManyToManyField):
            return {'widget': widgets.SelectMultipleDropdown, 'help_text': ''}
        
        if style == 'm2m_raw' and isinstance(db_field, ManyToManyField):
            db = kwargs.get('using')
            return {'widget': widgets.ManyToManyRawIdWidget(db_field.rel, self.admin_view, using=db), 'help_text': ''}
        if style == 'm2m_ajax' and isinstance(db_field, ManyToManyField):
            return {'widget': widgets.SelectMultipleAjax(db_field.rel, self.admin_view,False), 'help_text': ''}
        if style == 'm2m_ajax_multi' and isinstance(db_field, ManyToManyField):
            return {'widget': widgets.SelectMultipleAjax(db_field.rel, self.admin_view,True), 'help_text': ''}
        if style == 'm2m_select2' and isinstance(db_field, ManyToManyField):
            return {'widget': widgets.SelectMultipleDropselect, 'help_text': ''}
        return attrs


xadmin.site.register_plugin(M2MSelectPlugin, ModelFormAdminView)