"""
    Import needed things
"""
from django.urls import path
from page_speed_insights.views import page_speed_scrap_url, report_data, \
    detail_report_data, flag_data, PermissionAjaxDatatableView

app_name = "page_speed_insights"
urlpatterns = [
    path("report/", page_speed_scrap_url, name="report"),
    path("show_data/<int:pk>/", report_data, name="show_data"),
    path('ajax_datatable/permissions/<int:pk>/', PermissionAjaxDatatableView.as_view(), name="ajax_datatable_permissions"),
    path("detail_data/<int:pk>/", detail_report_data, name="detail_data"),
    path("flag_data/", flag_data, name="flag_data"),
]
