from django.urls import path
from . import views

app_name = "stockapp"

urlpatterns = [
    path("", views.stock_data_form, name="form"),
]

