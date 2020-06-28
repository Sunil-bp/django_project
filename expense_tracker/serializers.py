from rest_framework import serializers
from expense_tracker.models import Subcategory,Category,FinanceProfile\
    ,Account,AccountCategory,AccountSubcategory,ExpenseRecord,ExpenseTransfer
from users.models import Profile
from rest_framework.serializers import (
EmailField,
CharField,
HyperlinkedIdentityField,
ModelSerializer,
SerializerMethodField,
ValidationError
)


from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Category
        fields = "__all__"



class UserSerializer(serializers.ModelSerializer):
    # user_name = serializers.RelatedField(source="User",read_only=True)
    class Meta:
        model =User
        fields = ['username','email']


class FinanceProfileSerializer(serializers.ModelSerializer):
    # user_name = serializers.RelatedField(source="User",read_only=True)
    class Meta:
        model =FinanceProfile
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model =Account
        fields = "__all__"


class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =AccountCategory
        fields = "__all__"


class AccountSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =AccountSubcategory
        fields = "__all__"


class ExpenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model =ExpenseRecord
        fields = "__all__"


class ExpenseTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model =ExpenseTransfer
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        username = data.get('username',None)
        password = data.get('password', None)
        if not username:
            raise ValidationError("A username is require to login ")

        user = User.objects.filter(username=username)
        print(user)
        if user.exists() and user.count()==1:
            user = user.first()
        else:
            raise ValidationError("User is not valid ")
        if user:
            if not user.check_password(password):
                raise ValidationError("Credentials are not proper ")
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        data["token"] = "some random  token "
        return data


