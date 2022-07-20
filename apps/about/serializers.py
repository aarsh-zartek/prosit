from rest_framework import serializers

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.about.models import FAQ, Company, ContactForm


class FAQSerializer(DynamicFieldsModelSerializer):

	class Meta:
		model = FAQ
		fields = (
			"company", "question", "answer"
		)


class CompanySerializer(DynamicFieldsModelSerializer):
	faqs = serializers.SerializerMethodField()

	def get_faqs(self, instance: Company):
		return FAQSerializer(
				instance.faqs.all(),
				exclude=("company",),
				many=True
			).data
	
	class Meta:
		model = Company
		fields = (
			"home_page_title", "home_page_text",
			"contact_number", "about_the_company",
			"address", "faqs",
			"terms_and_conditions", "privacy_policy",
			"banner_title", "banner_text"
		)


class ContactFormSerializer(serializers.ModelSerializer):

	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = ContactForm
		fields = ("id", "name", "email", "phone_number", "message", "created")
