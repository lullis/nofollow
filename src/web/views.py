from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse

from cindy.models import Link
from cindy.serializers import URLSubmissionSerializer
from cindy import tasks


class HomeView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        is_logged = self.request.user.is_authenticated
        return reverse(
            'dashboard' if is_logged else 'login', request=self.request
        )


class LinkListView(LoginRequiredMixin, ListView):
    template_name = 'web/links.tmpl.html'
    paginate_by = 100

    def get_queryset(self, *args, **kw):
        return self.request.user.entry_set.order_by('-created')


class FeedListView(LoginRequiredMixin, ListView):
    template_name = 'web/feeds.tmpl.html'
    paginate_by = 100

    def get_queryset(self, *args, **kw):
        return self.request.user.userfeed_set.order_by('-created')


class SubmissionView(CreateAPIView):
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = URLSubmissionSerializer
    template_name = 'web/submit.tmpl.html'

    def get(self, request, **kw):
        serializer = self.get_serializer()
        return Response({'serializer': serializer})

    def post(self, request, **kw):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            tasks.handle_url_submission.delay(
                self.request.user.id, serializer.validated_data['url']
            )
            return redirect(reverse('dashboard', request=self.request))
        else:
            return Response(
                {'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST
            )


class LinkView(DetailView):
    template_name = 'web/read.tmpl.html'
    model = Link

    def get_object(self, *args, **kw):
        return get_object_or_404(
            Link, pk=self.kwargs['id'], processed_on__isnull=False
        )
