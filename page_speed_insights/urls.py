"""
    Import needed things
"""
from django.urls import path
from page_speed_insights.views import page_speed_scrap_url, report_data, \
    detail_report_data, flag_data

app_name = "page_speed_insights"
urlpatterns = [
    path("report/", page_speed_scrap_url, name="report"),
    path("show_data/", report_data, name="show_data"),
    path("detail_data/<int:pk>/", detail_report_data, name="detail_data"),
    path("flag_data/", flag_data, name="flag_data"),
]
