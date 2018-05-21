from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from tenant_report.views.web_views import (
    ReportListView,
    Report09DetailView
)
from tenant_report.views.csv_views import (
    random_sample_streaming_csv_view,
    report_09_streaming_csv_view
)

urlpatterns = (
    url(r'^reports$', ReportListView.as_view(), name='workery_tenant_reports_list_master'),
    url(r'^report/9/$', Report09DetailView.as_view(), name='workery_tenant_report_09_detail_master'),

    url(r'^report/9/csv-download$', report_09_streaming_csv_view, name='workery_tenant_report_09_download_csv_file_api_endpoint'),
)