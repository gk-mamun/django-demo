# context_processors.py
def mvoh_runs_in_session(request):
    # Fetch 'runs' from the session if it exists
    mvoh_runs = request.session.get('mvoh_runs', [])
    
    return {
        'session_mvoh_runs': mvoh_runs
    }