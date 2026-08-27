from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.response import Response
from .tasks import long_task
from rest_framework.views import APIView
from .tasks import add
from .services import build_task_status
from .tasks import generate_report_file
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from config.celery import app as celery_app
from celery.result import AsyncResult

from .models import (
    HeaderSetting, HeaderMenu, HeroSection, Result,
    ServiceSection, ServiceItem, WhyChooseUsSection,
    WhyChooseUsFeature, BannerNotification, Partner,
    Testimonial, ConsultancyRequest, NewsletterSubscriber, FooterLink
)

from .serializers import (
    HeaderSettingSerializer, HeaderMenuSerializer, HeroSectionSerializer,
    ResultSerializer, ServiceSectionSerializer, ServiceItemSerializer,
    WhyChooseUsSectionSerializer, WhyChooseUsFeatureSerializer,
    BannerNotificationSerializer, PartnerSerializer, TestimonialSerializer,
    ConsultancyRequestSerializer, NewsletterSubscriberSerializer, FooterLinkSerializer,
    AddTaskSerializer , TaskAccepedSerializer
)
from .cache_utils import build_cache_key

CACHE_TTL = 30


class BaseCustomAPIView(generics.ListCreateAPIView):
    pagination_class = None
    cache_enabled = True

    def get_cache_prefix(self):
        return f"landing:{self.__class__.__name__.lower()}:list"

    def list(self, request, *args, **kwargs):
        if self.cache_enabled:
            key = build_cache_key(self.get_cache_prefix(), request)
            cached_data = cache.get(key)

            if cached_data is not None:
                return Response({
                    "success": True,
                    "message": "Ma'lumotlar muvaffaqiyatli olindi (cache)",
                    "data": cached_data
                }, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not serializer.data:
            return Response({
                "success": False,
                "message": "Ma'lumotlar topilmadi",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        if self.cache_enabled:
            key = build_cache_key(self.get_cache_prefix(), request)
            cache.set(key, serializer.data, timeout=CACHE_TTL)

        return Response({
            "success": True,
            "message": "Ma'lumotlar muvaffaqiyatli olindi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            
            if self.cache_enabled:
                cache.delete_pattern(f"{self.get_cache_prefix()}:*")

            return Response({
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli saqlandi",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Ma'lumot saqlashda xatolik yuz berdi",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class HeaderSettingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeaderSetting.objects.all()
    serializer_class = HeaderSettingSerializer


class HeaderSettingView(BaseCustomAPIView):
    queryset = HeaderSetting.objects.all()
    serializer_class = HeaderSettingSerializer


class HeaderMenuView(BaseCustomAPIView):
    queryset = HeaderMenu.objects.all()
    serializer_class = HeaderMenuSerializer


class HeroSectionView(BaseCustomAPIView):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer


class ResultView(BaseCustomAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class ServiceSectionView(BaseCustomAPIView):
    queryset = ServiceSection.objects.all()
    serializer_class = ServiceSectionSerializer


class ServiceItemView(BaseCustomAPIView):
    queryset = ServiceItem.objects.all()
    serializer_class = ServiceItemSerializer


class WhyChooseUsSectionView(BaseCustomAPIView):
    queryset = WhyChooseUsSection.objects.all()
    serializer_class = WhyChooseUsSectionSerializer


class WhyChooseUsFeatureView(BaseCustomAPIView):
    queryset = WhyChooseUsFeature.objects.all()
    serializer_class = WhyChooseUsFeatureSerializer


class BannerNotificationView(BaseCustomAPIView):
    queryset = BannerNotification.objects.all()
    serializer_class = BannerNotificationSerializer


class PartnerView(BaseCustomAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class TestimonialView(BaseCustomAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class FooterLinkView(BaseCustomAPIView):
    queryset = FooterLink.objects.all()
    serializer_class = FooterLinkSerializer




class ConsultancyRequestView(BaseCustomAPIView):
    queryset = ConsultancyRequest.objects.all()
    serializer_class = ConsultancyRequestSerializer
    cache_enabled = False  


class NewsletterSubscriberView(BaseCustomAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    cache_enabled = False  



class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Yangi metodni shu yerga qo'shamiz
    def _get_task_status(self, request, task_id):
        if not task_id:
            return Response({"error": "Task ID berilmagan"}, status=400)
            
        task_result = AsyncResult(task_id)
        
        result_data = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return Response(result_data)

    def get(self, request, task_id=None):
        return self._get_task_status(request, task_id)

    def post(self, request, task_id=None):
        return self._get_task_status(request, task_id)

class AddTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer= AddTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        async_result = add.delay(
            serializer.validated_data["x"],
            serializer.validated_data["y"],

        )

        return Response(
            {
                "success": True,
                "message": "Vazifa qabul qilindi",
                "task_id": async_result.id,
                "status_url": f"/api/tasks/{async_result.id}/"
            },
            status=status.HTTP_202_ACCEPTED
        )


class TaskProgressView(APIView):
    permission_classes= [IsAuthenticated]


    def get(self, request, task_id):
        return Response(build_task_status(task_id)) 
    
    def delete(self, request, task_id):
        celery_app.control.revoke(task_id, terminate=True, signal="SIGTERM")

        
        return Response(
            {
                "success": True,
                "message": "Progress task ishga tushirildi",
                "task_id":task_id.id,
                "status": "REVOKED"
            },
            status=status.HTTP_202_ACCEPTED
        )


class GeneralReportView(APIView):
    def post(self, request):
        filename = request.data.get("filename", "hisobot.txt")
        res = generate_report_file.delay(filename)
        return Response(
            {
                "success": True,
                "message": "Fayl yaratish vazifasi fonda ishga tushdi",
                "task_id": res.id,
                "status_url": f"/api/tasks/{res.id}/"
            },
            status=status.HTTP_202_ACCEPTED
        )