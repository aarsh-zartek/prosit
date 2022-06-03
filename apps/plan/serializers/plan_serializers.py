from rest_framework import serializers

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.plan.models.diet_plan import DietPlan, PlanCategory

from lib.choices import PLAN_TYPES

class PlanCategorySerializer(DynamicFieldsModelSerializer):

	class Meta:
		model = PlanCategory
		fields = (
			"name", "instruction_text_english", "instruction_text_malayalam",
			"instruction_audio_english", "instruction_audio_malayalam",
			"instruction_pdf_english", "instruction_pdf_malayalam",
			"preparation_text_english", "preparation_text_malayalam",
			"preparation_audio_english", "preparation_audio_malayalam",
			"preparation_pdf_english", "preparation_pdf_malayalam",
		)


class DietPlanSerializer(DynamicFieldsModelSerializer):

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
		fields = ("name", )
	
	def create(self, validated_data):
		return super().create(validated_data)