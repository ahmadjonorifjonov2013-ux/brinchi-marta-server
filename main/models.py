from django.db import models


class HeaderSetting(models.Model):
    logo_title = models.CharField(max_length=100, default="Brainwave.io")
    button_text = models.CharField(max_length=100, default="Get started now")
    button_link = models.URLField(blank=True, null=True)


class HeaderMenu(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=255, default="#")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class HeroSection(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    button_text = models.CharField(max_length=100, default="Get started now")
    button_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='hero/')


class Result(models.Model):
    title = models.CharField(max_length=100)
    label = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ServiceSection(models.Model):
    title = models.CharField(max_length=255, default="Services we offer for you")
    description = models.TextField()


class ServiceItem(models.Model):
    section = models.ForeignKey(ServiceSection, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='services/')
    link = models.CharField(max_length=255, default="#", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class WhyChooseUsSection(models.Model):
    title = models.CharField(max_length=255, default="Why you should choose us?")
    description = models.TextField()
    video_preview = models.ImageField(upload_to='why_us/')
    video_url = models.URLField(blank=True, null=True)


class WhyChooseUsFeature(models.Model):
    section = models.ForeignKey(WhyChooseUsSection, on_delete=models.CASCADE, related_name='features')
    number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class BannerNotification(models.Model):
    tag = models.CharField(max_length=50, default="NEW")
    text = models.CharField(max_length=255)
    link_text = models.CharField(max_length=100)
    link_url = models.URLField(blank=True, null=True)


class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Testimonial(models.Model):
    quote = models.TextField()
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ConsultancyRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    service_needed = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FooterLink(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255, default="#")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']