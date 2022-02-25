"""
  import needed things
"""
from django.core import management


def ReportRunning():
    """
        ReportRunning
    """
    management.call_command('report_three_days')
