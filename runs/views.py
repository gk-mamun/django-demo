from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from .models import Run
from demosite.views import process_form
from django.http import Http404

# Create your views here.
def runs_view(request):

    runs = Run.objects.filter(user_id=request.user.id)

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
    
    return render(request, 'template-parts/run-list.html', {'runs': runs})  
    

def session_mvoh_run(request, id):

    runs = request.session.get('mvoh_runs', [])
    
    # Find the run with the specified ID
    run = next((run for run in runs if run['run_id'] == id), None)

    tciker_data = run.get('form_data').get('ticker_data')
    
    sector_data = {}
 
    for item in tciker_data:
        sector = item['sector']
        if sector in sector_data:
            sector_data[sector] += 1
        else:
            sector_data[sector] = 1

    # Convert the sector_data dictionary into the desired format (list of dictionaries)
    sector_data_list = [{'name': sector, 'value': count} for sector, count in sector_data.items()]

    if run is None:
        raise Http404("Run not found")
    
    saved_runs_with_output = Run.objects.filter(user_id=request.user.id).exclude(output_data__isnull=True).exclude(output_data__exact='').count()

    context = {
        'run': run,
        'sector_data': sector_data_list,
        'saved_runs_with_output': saved_runs_with_output
    }

    # Render the run data in a template, for example
    return render(request, 'mvoh_run_template.html', context)


def save_session_run_view(request):
    user_id = request.user.id 
    title = request.POST.get('title')
    input_data = process_form(request)
    session_run_id = request.POST.get('session_run_id')

    runs = request.session.get('mvoh_runs', [])
    
    # Find the run with the specified ID
    run = next((run for run in runs if run['run_id'] == int(session_run_id)), None)


    new_run = Run(
        user_id=user_id,
        title=title,
        input_data=input_data
    )
    if(request.POST.get('save_output') != None and request.POST.get('save_output') == 'on' ):
        output_data=run.get('output')
        new_run.output_data=output_data
    new_run.save()

    new_runs = [r for r in runs if r['run_id'] != int(session_run_id)]
    request.session['mvoh_runs'] = new_runs

    saved_runs = Run.objects.filter(user_id=request.user.id)

    context = {
        "runs": saved_runs
    }
    return render(request, 'runs_mvoh.html', context)

