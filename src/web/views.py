from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView, DetailView
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status

from cindy.models import Link
from cindy.serializers import URLSubmissionSerializer
from cindy import tasks


class HomeView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        is_logged = self.request.user.is_authenticated
        return reverse('dashboard' if is_logged else 'login')


class DashboardView(LoginRequiredMixin, DetailView):
    PAGE_SIZE = 20
    template_name = 'web/dashboard.tmpl.html'

    def get_object(self, *args, **kw):
        return self.request.user

    def get_context_data(self, *args, **kw):
        context = super().get_context_data(*args, **kw)
        user = self.get_object()
        context.update({
            'links': user.entry_set.order_by('-created')[:self.PAGE_SIZE],
            'feeds': user.userfeed_set.order_by('-created')[:self.PAGE_SIZE]
            })
        return context


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
            return Response(status=status.HTTP_201_CREATED, headers={
                'Location': reverse('dashboard')
                })
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
