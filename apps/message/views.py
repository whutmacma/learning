from django.shortcuts import render
from message.models import UserMessage
# Create your views here.

def getForm(request):
	all_messages = UserMessage.objects.all()
	if all_messages:
	   message = all_messages[0]
	   

	return render(request, 'message_form.html', {
	      "my_message":message
	})

