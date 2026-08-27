from django.urls import path
from . import views

urlpatterns = [
    path('header/', views.HeaderSettingView.as_view()),
    path('header/<int:pk>/', views.HeaderSettingDetailView.as_view()),
    path('header-menu/', views.HeaderMenuView.as_view()),
    path('hero/', views.HeroSectionView.as_view()),
    path('results/', views.ResultView.as_view()),
    path('services/', views.ServiceSectionView.as_view()),
    path('services/items/', views.ServiceItemView.as_view()),
    path('why-us/', views.WhyChooseUsSectionView.as_view()),
    path('why-us/features/', views.WhyChooseUsFeatureView.as_view()),
    path('banner-notifications/', views.BannerNotificationView.as_view()),
    path('partners/', views.PartnerView.as_view()),
    path('testimonials/', views.TestimonialView.as_view()),
    path('consultancy-requests/', views.ConsultancyRequestView.as_view()),
    path('newsletter/subscribers/', views.NewsletterSubscriberView.as_view()),
    path('footer/links/', views.FooterLinkView.as_view()),
    path('tasks/add/', views.AddTaskView.as_view(), name="task-add"),
    path('tasks/<str:task_id>/', views.TaskStatusView.as_view(), name='task-status-path'),
    path('tasks/progress/', views.TaskProgressView.as_view(), name="task-progress"),
    path('tasks/generate-report/', views.GeneralReportView.as_view(), name="generate-report"),
    
]