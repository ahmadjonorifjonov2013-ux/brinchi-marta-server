from django.core.management.base import BaseCommand
from django.apps import apps
from faker import Faker

class Command(BaseCommand):
    help = "MAIN ilovasidagi barcha modellarga 5 tadan test ma'lumot qo'shadi"

    def handle(self, *args, **kwargs):
        fake = Faker()
        # MAIN ilovangizdagi barcha modellarni olamiz
        app_models = apps.get_app_config('main').get_models()

        for model in app_models:
            model_name = model.__name__
            self.stdout.write(f"{model_name} modeliga ma'lumot qo'shilmoqda...")
            
            for _ in range(5):
                data = {}
                for field in model._meta.get_fields():
                    # Id va avto-to'ladigan maydonlarni o'tkazib yuboramiz
                    if field.is_relation or field.auto_created or not hasattr(field, 'type'):
                        continue
                    
                    # Maydon turiga qarab soxta qiymat beramiz
                    internal_type = field.get_internal_type()
                    if internal_type in ['CharField', 'TextField']:
                        data[field.name] = fake.sentence(nb_words=3)
                    elif internal_type == 'IntegerField':
                        data[field.name] = fake.random_int(min=1, max=100)
                    elif internal_type == 'BooleanField':
                        data[field.name] = fake.boolean()
                    elif internal_type == 'URLField':
                        data[field.name] = fake.url()
                    elif internal_type == 'EmailField':
                        data[field.name] = fake.email()

                try:
                    model.objects.create(**data)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  -> {model_name} uchun ba'zi majburiy maydonlarni to'ldirib bo'lmadi: {e}"))

            self.stdout.write(self.style.SUCCESS(f"✔ {model_name} modeliga 5 ta ma'lumot qo'shildi!"))

        self.stdout.write(self.style.SUCCESS("\nBarcha modellar muvaffaqiyatli to'ldirildi!"))