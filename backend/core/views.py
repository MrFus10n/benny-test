from django.views.generic import TemplateView
from django.middleware.csrf import get_token\


class React(TemplateView):
    template_name = 'core/react.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['config'] = {
            'CSRF': get_token(self.request),
        }
        return ctx
