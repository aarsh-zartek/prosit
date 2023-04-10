from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from phonenumber_field.serializerfields import PhoneNumberField

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.plan.models import DietPlan
from apps.plan.serializers.diet_plan_serializers import DietPlanSerializer
from apps.users.models import User, DailyActivity, UserHealthReport, Profile
from apps.users.serializers.profile_serializer import ProfileSerializer
from lib.choices import GENDER, PLAN_TYPES


class UserSerializer(DynamicFieldsModelSerializer):
    """User model serializer for users."""

    password = serializers.CharField(required=False, write_only=True)
    phone_number = PhoneNumberField(required=False)
    profile = ProfileSerializer(required=False)
    active_subscription = serializers.SerializerMethodField()
    active_plan = serializers.SerializerMethodField()
    plan_name = serializers.SerializerMethodField()

    def get_active_subscription(self, instance: User) -> bool:
        return True if instance.active_subscription else False

    def get_active_plan(self, instance: User) -> bool:
        return True if instance.active_plan else False

    def get_plan_name(self, instance: User) -> str | None:
        sub = instance.active_subscription
        plan_name = None
        if not sub:
            return plan_name
        try:
            plan = DietPlan.objects.get(id=sub.receipt["plan_id"])
            if plan.plan_type == PLAN_TYPES.main_category:
                plan_name = plan.name
            else:
                plan_name = plan.parent.name
        except:
            try:
                plan_name = instance.active_plan.name
            except:
                pass
        return plan_name

    def validate_email(self, email):
        email_filter = User.objects.filter(email=email)
        if self.instance and email_filter.exclude(pk=self.pk).exists():
            raise serializers.ValidationError("Email already exists.")
        return email

    class Meta:
        model = User
        fields = (
            "id", "uid", "display_name", "password", "phone_number",
            "email", "first_name", "last_name", "profile",
            "profile_picture", "active_subscription", "active_plan",
            "plan_name"
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        profile, _ = Profile.objects.create(user=instance)
        return instance

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile, _ = Profile.objects.get_or_create(user=instance)
            serializer = ProfileSerializer(instance=profile, data=profile_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        user = super().update(instance, validated_data)
        return user


class UserHealthReportSerializer(DynamicFieldsModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_hemoglobin(self, hemoglobin):
        if not 1 < int(hemoglobin) < 30:
            raise serializers.ValidationError("Enter a value between 1 and 30")
        return hemoglobin

    def validate(self, attrs: dict) -> dict:
        user: User = self.context.get('user')
        pcod_pcos = attrs.get('pcod_pcos', None)
        image = attrs.get("image", "not_present")
        workout_time = attrs.get("workout_time", None)

        if not user.active_subscription:
            raise serializers.ValidationError("No Active Subscription found for this user")

        if user.active_subscription.health_report:
            raise serializers.ValidationError("You already have an active subscription")

        if image is None:
            attrs.pop("image")

        if (pcod_pcos is None) and (user.profile.gender == GENDER.female):
            raise serializers.ValidationError("You must provide `pcod_pcos` field for the female user")
        elif pcod_pcos and (user.profile.gender == GENDER.male):
            attrs.pop('pcod_pcos')

        plan_id = user.active_subscription.receipt["plan_id"]
        try:
            subscribed_for = DietPlan.objects.get(id=plan_id)
        except DietPlan.DoesNotExist:
            raise serializers.ValidationError("No Plan exists")

        if workout_time is None and subscribed_for.is_gym_plan:
            raise serializers.ValidationError(f"Workout Time required for {subscribed_for.name}")
        if workout_time is not None and not subscribed_for.is_gym_plan:
            try:
                attrs.pop("workout_time")
            except KeyError:
                pass

        return attrs

    class Meta:
        model = UserHealthReport
        fields = (
            "user", "vitamin_b12", "vitamin_d", "hemoglobin", "uric_acid",
            "creatin", "fasting_blood_sugar", "cholesterol", "thyroid_tsh", "pcod_pcos",
            "workout_time", "dry_skin", "image", "extra_info"
        )


class DailyActivitySerializer(DynamicFieldsModelSerializer):
    """To track daily user activity

    `weight` is a non-editable field

    `date` must be less than or equal to today's date
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_date(self, date_value):
        if date_value > timezone.now():
            raise serializers.ValidationError("Date must be less than or equal to today's date")
        return date_value

    class Meta:
        model = DailyActivity
        fields = ("user", "weight", "date")
        validators = [
            UniqueTogetherValidator(
                queryset=DailyActivity.objects.all(),
                fields=["user", "date"]
            )
        ]


class UserDietPlanSerializer(DynamicFieldsModelSerializer):
    """Get User Subscribed Plan Details"""

    my_plan = serializers.SerializerMethodField()
    subscription_status = serializers.SerializerMethodField()

    def get_my_plan(self, instance: User):
        plan = instance.active_subscription.plan
        return DietPlanSerializer(
            instance=plan,
            exclude=("queries", "parent", 'plan_type'),
            context=self.context
        ).data

    def get_subscription_status(self, instance: User) -> str:
        return instance.active_subscription.get_subscription_status_display()


    class Meta:
        model = User
        fields = ("my_plan", "subscription_status")
