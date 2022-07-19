from rest_framework import serializers

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.plan.models.diet_plan import DietPlan, PlanCategory, QuestionAnswer

from lib.choices import PLAN_TYPES


class PlanCategorySerializer(DynamicFieldsModelSerializer):

	class Meta:
		model = PlanCategory
		fields = (
			"id", "name",
			"per_day_instructions_english", "per_day_instructions_malayalam",
			"instruction_text_english", "instruction_text_malayalam",
			"instruction_audio_english", "instruction_audio_malayalam",
			"instruction_pdf_english", "instruction_pdf_malayalam",
			"preparation_text_english", "preparation_text_malayalam",
			"preparation_audio_english", "preparation_audio_malayalam",
			"preparation_pdf_english", "preparation_pdf_malayalam",
			"fields_required"
		)


class QuestionAnswerSerializer(DynamicFieldsModelSerializer):

	class Meta:
		model = QuestionAnswer
		fields = ('diet_plan', 'question', 'answer')


class DietPlanSerializer(DynamicFieldsModelSerializer):

	category = PlanCategorySerializer(read_only=True)
	queries = serializers.SerializerMethodField()
	
	def get_queries(self, instance: DietPlan):
		serializer = QuestionAnswerSerializer(
			instance.question_answers.all(),
			exclude=("diet_plan",),
			many=True
		)
		return serializer.data


	def validate(self, attrs: dict):
		plan_type = attrs.get("plan_type", None)
		parent = attrs.get("parent", None)

		if plan_type == PLAN_TYPES.sub_category and parent is None:
			raise serializers.ValidationError("Parent must be specified for Sub category Plan Type")
		
		if plan_type == PLAN_TYPES.category and parent is not None:
			attrs.pop('parent')
		
		return attrs
	
	class Meta:
		model = DietPlan
		fields = (
			"id", "name", "category", "plan_type", "parent",
			"queries", "value", "product_identifer"
		)
	
	def create(self, validated_data):
		return super().create(validated_data)


class DietPlanListSerializer(DynamicFieldsModelSerializer):

	category_name = serializers.CharField(source="category.name")
	sub_categories = serializers.SerializerMethodField()

	def get_sub_categories(self, instance: DietPlan) -> list:
		serializer = DietPlanSerializer(
			instance.sub_categories.all(),
			many=True,
			fields=("id", "name",)
		)
		return serializer.data or []

	class Meta:
		model = DietPlan
		fields = (
			"id", "name", "category_name",
			"plan_type", "sub_categories",
		)
