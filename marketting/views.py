from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect


from .forms import MarkettingPreferenceForm
from .mixins import CsrfExemptMixin
from .models import MarkettingPreference
from .utils import Mailchimp
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_AUDIENCE_ID", None)

class MarkettingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarkettingPreferenceForm
    template_name = 'marketting/subscription.html' # yeah create this
    success_url = '/email-subscription/'
    success_message = 'Your email preferences have been updated.'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        # messages.success(self.request, "Preferences Updated Successfully" )
        if not user.is_authenticated:
            return redirect("/login/?next=/email-subscription/") # HttpResponse("Not allowed", status=400)
        return super(MarkettingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarkettingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarkettingPreference.objects.get_or_create(user=user) # get_absolute_url
        return obj


class MailchimpWebhookView(CsrfExemptMixin, View): # HTTP GET -- def get() CSRF?????
    def get(self, request, *args, **kwargs):
        return HttpResponse("GET not allowed", status=200)
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subcription_status(email)
            sub_status  = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed  = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed  = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarkettingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed=is_subbed,
                            mailchimp_subscribed=mailchimp_subbed,
                            mailchimp_msg=str(data))
        return HttpResponse("Thank you", status=200)
