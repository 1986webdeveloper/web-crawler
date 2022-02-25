import os
import ast
from django import template

register = template.Library()


@register.filter(name="first_contentful_paint")
def first_contentful_paint(value):
    if value:
       value = value['first-contentful-paint']['displayValue']
    return value


@register.filter(name="first_contentful_paint_des")
def first_contentful_paint_des(value):
    if value:
       value = value['first-contentful-paint']['description']
    return value


@register.filter(name="speed_index")
def speed_index(value):
    if value:
       value = value['speed-index']['displayValue']
    return value


@register.filter(name="speed_index_des")
def speed_index_des(value):
    if value:
       value = value['speed-index']['description']
    return value


@register.filter(name="largest_contentful_paint")
def largest_contentful_paint(value):
    if value:
       value = value['largest-contentful-paint']['displayValue']
    return value


@register.filter(name="largest_contentful_paint_des")
def largest_contentful_paint_des(value):
    if value:
       value = value['largest-contentful-paint']['description']

    return value


@register.filter(name="total_blocking_time")
def total_blocking_time(value):
    if value:
       value = value['total-blocking-time']['displayValue']
    return value


@register.filter(name="total_blocking_time_des")
def total_blocking_time_des(value):
    if value:
       value = value['total-blocking-time']['description']
    return value


@register.filter(name="cumulative_layout_shift")
def cumulative_layout_shift(value):
    if value:
       value = value['cumulative-layout-shift']['displayValue']
    return value


@register.filter(name="cumulative_layout_shift_des")
def cumulative_layout_shift_des(value):
    if value:
       value = value['cumulative-layout-shift']['description']
    return value


@register.filter(name="server_response_time")
def server_response_time(value):
    if value:
       value = value['server-response-time']['displayValue']
    return value


@register.filter(name="server_response_time_des")
def server_response_time_des(value):
    if value:
       value = value['server-response-time']['description']
    return value


@register.filter(name="mainthread_work_breakdown")
def mainthread_work_breakdown(value):
    if value:
       value = value['mainthread-work-breakdown']['displayValue']
    return value


@register.filter(name="mainthread_work_breakdown_des")
def mainthread_work_breakdown_des(value):
    if value:
       value = value['mainthread-work-breakdown']['description']
    return value


@register.filter(name="unused_javascript")
def unused_javascript(value):
    if value:
       value = value['unused-javascript']['displayValue']
    return value


@register.filter(name="unused_javascript_des")
def unused_javascript_des(value):
    if value:
       value = value['unused-javascript']['description']
    return value


@register.filter(name="dom_size")
def dom_size(value):
    if value:
       value = value['dom-size']['displayValue']
    return value
