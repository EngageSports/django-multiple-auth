#!/bin/bash
PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.test_settings django-admin test
