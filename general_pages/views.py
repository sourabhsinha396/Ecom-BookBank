# Django's built in imports
from django.shortcuts import render
from django.contrib import messages

# This Folder imports
from .forms import ContactUsModelForm


def home(request):
    # session_first_name = request.session.get('first_name','Dear User')
    # get is good, request.session['first_name'] may give error if first_name DoesNotExist
    # messages.success(request,'Hi {}'.format(session_first_name))
    context = {'page_name':'I love books 3000'}
    return render(request,'general_pages/home.html',context)

def aboutus(request):
    context = {'page_name':'I love books 3000'}
    return render(request,'general_pages/aboutus.html',context)


def contact(request):
    if request.method == "POST":
        form = ContactUsModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Submitted" )
        if form.errors:
            print(form.errors)
            messages.error(request, "These Error Occured" )
            messages.warning(request, "{}".format(form.errors))
        context = {'page_name':'Contact Us','form':form}
        return render(request,'general_pages/contactus.html',context)
    else:
        context = {'page_name':'Contact Us'}
        return render(request,'general_pages/contactus.html',context)
