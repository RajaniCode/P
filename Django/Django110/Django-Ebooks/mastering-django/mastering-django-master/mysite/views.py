import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from mysite.forms import ContactForm
from django.core.mail import send_mail


def hello(request):
    return HttpResponse("Hello World!")


def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html',
                  {'hour_offset': offset, 'next_time': dt})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            """send_mail(
                cd['subject'],
                cd['message'],
                    cd.get('email', <a class="reference external" href="mailto:'noreply%40example.com">'noreply@example.com</a>'), 
                           [<a class="reference external" href="mailto:'siteowner%40example.com">'siteowner@example.com</a>'],
            )"""
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render(request, 'contact_form.html', {'form': form})
