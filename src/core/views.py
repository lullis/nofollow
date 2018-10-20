from django.views.generic import TemplateView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from . import serializers
from . import models


class ConversionView(CreateAPIView):
    serializer_class = serializers.ConverterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc = models.Document(serializer.data['url'])
        location = reverse('document-detail', request=request, kwargs={
            'doc_hash': doc.hexdigest
            })
        if not doc.is_processed:
            doc.process()
            return Response(status=status.HTTP_201_CREATED, headers={'Location': location})
        else:
            return Response(status=status.HTTP_303_SEE_OTHER, headers={'Location': location})


class DocumentView(TemplateView):
    template_name = 'converted.tmpl.html'

    def get_context_data(self, **kw):
        context = super(DocumentView, self).get_context_data(**kw)
        document = models.ConvertedDocument(kw.get('doc_hash'))
        with open(document.path) as doc_file:
            context['converted_document'] = doc_file.read()
        return context
