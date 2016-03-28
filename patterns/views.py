from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'patterns/index.html', {
        'button_data': {
            'label': 'A button',
            'type': 'Primary'
        },
        'alert_data': {
            'content': 'This is the alert'
        },
        'donation_amounts': {
            'name': 'donations',
            'options': [
                {
                    'name': 'donations',
                    'value': 50,
                    'label': '$50'
                },
                {
                    'name': 'donations',
                    'value': 75,
                    'label': '$75'
                },
                {
                    'name': 'donations',
                    'value': 200,
                    'label': '$200'
                }
            ]
        }
    })
