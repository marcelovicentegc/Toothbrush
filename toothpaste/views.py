import os
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.edit import CreateView
from toothpaste.forms import DocumentForm
from toothpaste.models import DocumentModel
from toothpaste.toilet_sink.soap import ToiletSink
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime, timedelta




class IndexView(FormView, CreateView):
    template_name = 'toothpaste/home.html'
    form_class = DocumentForm
    ToiletSink = ToiletSink()

    def get_success_url(self):
        document = self.object
        return reverse('result-detail', args=[document.uid,])

    def form_valid(self, form):
        form.save()
        return super(IndexView, self).form_valid(form)

    def upload_file(self, request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                document = form.cleaned_data['document']
                document.save(commit=True)
                return redirect(self.get_success_url())
        else: 
            form = DocumentForm()
        return render(request, self.template_name, {'form': form})




class AboutView(TemplateView):
    template_name = 'toothpaste/about.html'




class ResultView(DetailView, ToiletSink):
    template_name = 'toothpaste/result.html'
    model = DocumentModel
    queryset = model.objects.all()

    def get_queryset(self, **kwargs):
        return self.queryset.filter(date__gte=datetime.now()-timedelta(days=1))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uid'] = self.object.uid
        return context




class ChartData(APIView, DetailView, ToiletSink):
    authentication_classes = []
    permission_classes = []
    ToiletSink = ToiletSink()
    model = DocumentModel

    def get(self, request, pk, format=None):
        self.object = self.get_object()
        document = self.object.document.path
        f = self.ToiletSink.text_extractor(document)
        f = self.ToiletSink.final_cut(f)
        words = f[0]
        freqs = f[1]
        data = {
            'words': words,
            'freqs': freqs,
        }
        return Response(data)