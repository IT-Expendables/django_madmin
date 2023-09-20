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
    vue_context = {}

    def __init__(self, attrs=None, vue_context={}):
        super().__init__(attrs)
        self.vue_context = vue_context

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget_context = context.setdefault('widget', {})
        widget_attrs = widget_context.setdefault('attrs', {})
        id = widget_attrs.setdefault('id', 'id_{}'.format(get_random_string(8)))
        self.vue_context['id'] = id
        widget_context['vue_context'] = self.vue_context
        return context

    class Media:

        class MAdminJS:
            def __html__():
                js = VUE_DEV_URL if settings.DEBUG else static(VUE_JS)
                return '<script type="module" crossorigin src="{}"></script>'.format(js) if js else ''

        js = [MAdminJS]


class AsyncFileUpload(VueComponent):

    def __init__(self, attrs=None, vue_context={}):
        vue_context = {'check_upload_url': '/madmin/check_upload/', **vue_context, 'component': 'MFileUpload'}
        super().__init__(attrs, vue_context)


class AsyncImageUpload(AsyncFileUpload):

    def __init__(self, attrs=None, vue_context={}):
        vue_context = {'upload_type': 'image', **vue_context}
        super().__init__(attrs, vue_context)


class AsyncVideoUpload(AsyncFileUpload):

    def __init__(self, attrs=None, vue_context={}):
        vue_context = {'upload_type': 'video', **vue_context}
        super().__init__(attrs, vue_context)
