from django.db import models
from django.contrib.auth.models import User
from .utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)

import os

from uygulama.models import User, Log, email_verification
# Create your models here.



