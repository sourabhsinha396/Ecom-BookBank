from django.urls import path
from .views import MarkettingPreferenceUpdateView,MailchimpWebhookView
urlpatterns = [
    #############--------Function Based------###############
    path('email-subscription/',MarkettingPreferenceUpdateView.as_view(),name="subscription"),
    path('webhook-mailchimp/',MailchimpWebhookView.as_view(),name="webhook_mailchimp"),
    ]
