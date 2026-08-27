from rest_framework import serializers
from .models import HeaderSetting, HeaderMenu, HeroSection, Result, ServiceSection, ServiceItem, WhyChooseUsSection, WhyChooseUsFeature, BannerNotification, Partner, Testimonial, ConsultancyRequest, NewsletterSubscriber, FooterLink


class HeaderSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderSetting
        fields = '__all__'


class HeaderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderMenu
        fields = '__all__'


class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class ServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceItem
        fields = '__all__'


class ServiceSectionSerializer(serializers.ModelSerializer):
    items = ServiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceSection
        fields = '__all__'


class WhyChooseUsFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUsFeature
        fields = '__all__'


class WhyChooseUsSectionSerializer(serializers.ModelSerializer):
    features = WhyChooseUsFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = WhyChooseUsSection
        fields = '__all__'


class BannerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerNotification
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class ConsultancyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyRequest
        fields = '__all__'


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = '__all__'


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = '__all__'


class AddTaskSerializer(serializers.Serializer):
    x= serializers.IntegerField()
    y = serializers.IntegerField()


class TaskAccepedSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    state = serializers.CharField()
    states_url = serializers.CharField()



    