from django.shortcuts import render_to_response, RequestContext


# Create your views here.

def index(request):
    current_url = request.path
    return render_to_response('index.html', {'index_url': current_url}, context_instance=RequestContext(request))


def about(request):
    current_url = request.path
    return render_to_response('about.html', {'about_url': current_url}, context_instance=RequestContext(request))


def services(request):
    current_url = request.path
    return render_to_response('services.html', {'services_url': current_url}, context_instance=RequestContext(request))


def news(request):
    current_url = request.path
    return render_to_response('news.html', {'news_url': current_url}, context_instance=RequestContext(request))


def contact(request):
    current_url = request.path
    return render_to_response('contact.html', {'contact_url': current_url}, context_instance=RequestContext(request))


def right_connect(request):
    current_url = request.path
    return render_to_response('right_connect.html', {'right_connect_url': current_url},
                              context_instance=RequestContext(request))


def professional_resume(request):
    current_url = request.path
    return render_to_response('professional_resume.html', {'services_url': current_url},
                              context_instance=RequestContext(request))


def executive_service(request):
    current_url = request.path
    return render_to_response('executive_service.html', {'services_url': current_url},
                              context_instance=RequestContext(request))


def combo_services(request):
    current_url = request.path
    return render_to_response('combo_services.html', {'services_url': current_url},
                              context_instance=RequestContext(request))


def privacy_policy(request):
    current_url = request.path
    return render_to_response('privacy_policy.html', {'privacy_policy': current_url},
                              context_instance=RequestContext(request))