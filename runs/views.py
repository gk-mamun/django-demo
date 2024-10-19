from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from .models import Run
from demosite.views import process_form

# Create your views here.
def runs_view(request):

    runs = Run.objects.all()

    context = {
        "runs": runs
    }

    return render(request, 'runs_mvoh.html',  context)


def save_run_view(request):

    if request.method == 'POST':
        user_id = request.user.id 
        title = request.POST.get('title')
        json_data = process_form(request)

        new_run = Run(
            user_id=user_id,
            title=title,
            json_data=json_data
        )
        new_run.save()

        # Render the new row as HTML
        runs = Run.objects.all()  # Fetch the remaining runs
        
        return render(request, 'template-parts/run-list.html', {'runs': runs})

    return JsonResponse({'error': 'Invalid request'}, status=400)



def delete_run(request):
    run_id = request.POST.get('run_id')
    run = Run.objects.get(id=run_id)
    run.delete()
    
    runs = Run.objects.all()  # Fetch the remaining runs
    
    return render(request, 'template-parts/run-list.html', {'runs': runs})  # Render the updated template
    