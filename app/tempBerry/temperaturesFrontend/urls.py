from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.views import serve

# Redirect any request that goes into here to static/index.html
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='static/', permanent=False), name='index')
    # url(r'^$', TemplateView.as_view(template_name='index.html'))

    # serve index.htmla nd static things directly
    # taken from http://stackoverflow.com/a/40525517
    # and http://stackoverflow.com/questions/27065510/how-to-serve-static-files-with-django-that-has-hardcoded-relative-paths-on-herok/40525157#40525157

    # url(r'^$', serve,
    #     kwargs={'path': 'index.html'}),
    #
    # # static files (*.css, *.js, *.jpg etc.) served on /
    # url(r'^(?!/static/.*)(?P<path>.*\..*)$',
    #     RedirectView.as_view(url='/static/%(path)s')),
]