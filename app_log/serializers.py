from rest_framework import serializers
from rest_framework.serializers import (
EmailField,
CharField,
HyperlinkedIdentityField,
ModelSerializer,
SerializerMethodField,
ValidationError
)
from app_log.models import App_list,App_history
from django.contrib.auth.models import User


class AppListserializers(serializers.ModelSerializer):
    class Meta:
        model = App_list
        fields = "__all__"

class Apphistoryserializers(serializers.ModelSerializer):
    class Meta:
        model = App_history
        fields = "__all__"