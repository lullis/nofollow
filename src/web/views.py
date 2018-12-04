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

from boris.models import Link, CrawledItem
from boris.serializers import LinkSerializer
from core.tasks import handle_url_submission


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
        user_links = self.request.user.userlink_set.prefetch_related(
            'link', 'link__crawleditem_set'
        )

        return CrawledItem.objects.filter(id__in=[
            ul.link.crawleditem_set.order_by('-extraction_score').values_list(
                'id', flat=True
            ).first() for ul in user_links]).order_by('-link__userlink__created')


class FeedListView(LoginRequiredMixin, ListView):
    template_name = 'web/feeds.tmpl.html'
    paginate_by = 100

    def get_queryset(self, *args, **kw):
        return self.request.user.userfeed_set.order_by('-created')


class SubmissionView(CreateAPIView):
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = LinkSerializer
    template_name = 'web/submit.tmpl.html'

    def get(self, request, **kw):
        serializer = self.get_serializer()
        return Response({'serializer': serializer})

    def post(self, request, **kw):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            submitted_url = serializer.validated_data['url']
            user = self.request.user
            if user.userlink_set.filter(link__url=submitted_url).exists():
                return redirect(reverse('link-list', request=self.request))
            elif user.userfeed_set.filter(feed__url=submitted_url).exists():
                return redirect(reverse('feed-list', request=self.request))
            else:
                handle_url_submission.delay(user.id, submitted_url)
                return redirect(reverse('dashboard', request=self.request))
        else:
            return Response(
                {'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST
            )


class LinkView(DetailView):
    template_name = 'web/read.tmpl.html'
    model = Link

    def get_object(self, *args, **kw):
        return get_object_or_404(Link, pk=self.kwargs['id'])
