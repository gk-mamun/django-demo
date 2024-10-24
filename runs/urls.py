from django.urls import path

from .views import runs_view, save_run_view, delete_run, session_mvoh_run, save_session_run_view

urlpatterns = [
    path('', runs_view, name="runs_mvoh"),
    path('save-run/', save_run_view, name="save-run"),
    path('delete-run/', delete_run, name='delete-run'),
    path('session-mvoh-run/<int:id>/', session_mvoh_run, name='session-mvoh-run'),
    path('save-session-mvoh-run/', save_session_run_view, name='save-session-mvoh-run'),
]