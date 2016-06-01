from django.shortcuts import render_to_response, RequestContext


# Create your views here.

def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request))

def services(request):
    return render_to_response('services.html', {}, context_instance=RequestContext(request))
