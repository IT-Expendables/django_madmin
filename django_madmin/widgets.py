from django import forms
from django.templatetags.static import static
from django.conf import settings
from django.utils.crypto import get_random_string
from pathlib import Path


def get_vue_js():
    js_dir = Path(__file__).resolve().parent.joinpath('static/madmin/js')
    for p in js_dir.iterdir():
        if not p.name.startswith('index-'):
            continue
        return 'madmin/js/' + p.name


VUE_JS = get_vue_js()

VUE_DEV_URL = 'http://127.0.0.1:5199/src/main.js'


class VueComponent(forms.Widget):
    template_name = "madmin/vue_component.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget = context.get('widget')
        attrs = widget.setdefault('attrs', {})
        id = attrs.setdefault('id', 'id_{}'.format(get_random_string(8)))
        widget['id'] = id
        return context

    class Media:

        class MAdminJS:
            def __html__():
                dev = getattr(settings, 'MADMIN', {}).get('dev', False)
                js = VUE_DEV_URL if dev else static(VUE_JS)
                return '<script type="module" crossorigin src="{}"></script>'.format(js) if js else ''

        js = [MAdminJS]


class AsyncFileUpload(VueComponent):

    def get_context(self, name, value, attrs):
        prefix = getattr(settings, 'MADMIN', {}).get('upload_path_prefix', 'madmin')
        context = super().get_context(name, value, attrs)
        context.get('widget').update({
            'component': 'MFileUpload',
            'check_upload_url': '/{}/check_upload/'.format(prefix)
        })
        return context


class AsyncImageUpload(AsyncFileUpload):

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.get('widget').update({'upload_type': 'image'})
        return context


class AsyncVideoUpload(AsyncFileUpload):

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.get('widget').update({'upload_type': 'video'})
        return context


class AsyncMultiFileUpload(VueComponent):

    def get_context(self, name, value, attrs):
        prefix = getattr(settings, 'MADMIN', {}).get('upload_path_prefix', 'madmin')
        attrs = attrs or {}
        attrs.update({'class': 'sm:!w-[486px] w-full'})
        context = super().get_context(name, value, attrs)
        context.get('widget').update({
            'component': 'MMultiFileUpload',
            'check_upload_url': '/{}/check_upload/'.format(prefix),
        })
        return context
