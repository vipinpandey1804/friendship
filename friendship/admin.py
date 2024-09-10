from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models
for model_name, model in models.__dict__.items():
    try:
        admin.site.register(model) if str(
            type(model)) == "<class 'django.db.models.base.ModelBase'>" else None
    except admin.sites.AlreadyRegistered:
        continue
    except Exception as e:
        # print(e)
        continue