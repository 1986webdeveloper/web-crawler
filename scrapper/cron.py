from django.core import management


def ReportRunning():
    management.call_command('report_three_days')

