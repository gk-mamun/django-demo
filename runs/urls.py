from django.urls import path

from .views import runs_view, save_run_view, delete_run

urlpatterns = [
    path('', runs_view, name="runs_mvoh"),
    path('save-run/', save_run_view, name="save-run"),
    path('delete-run/', delete_run, name='delete-run'),
]