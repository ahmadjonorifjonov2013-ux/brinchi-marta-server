import time
from celery import shared_task
import os
from django.conf import settings

@shared_task
def add(x, y):
    time.sleep(30)
    return x + y

@shared_task(bind=True)
def long_task(self, total_steps=10):
    for i in range(1, total_steps+ 1):
        time.sleep(1)
        self.update_state(state= "PROGRESS",
        meta={
            "current":i,
            "total": total_steps,
            "percent": round((i/ total_steps) * 100, 1),
            "stage": f"{i}/{total_steps} bosqich bajarilmoqda..."
        })
        return {"status":"Tugadi", "total_processed":total_steps}



@shared_task(bind=True)
def generate_report_file(self, filename="hisobot.txt"):
    media_dir = os.path.join(settings.BASE_DIR, 'media')
    os.makedirs(media_dir, exist_ok=True)
    file_path = os.path.join(media_dir, filename)

    total_lines = 5
    with open(file_path,"w", encoding="utf-8") as f:
        f.write("=== AVTOMATIK YARATILGAN HISOBOT ===\n\n")
        for i in range(1, total_lines + 1):
            time.sleep(1)
            f.write(f"{i}-qator: Ma'lumotlar qayta ishlandi va yozildi.\n")
            self.update_state(
                state="PROGRESS",
                meta={
                    "current":i,
                    "total": total_lines,
                    "percent": round((i / total_lines) *100, 1),
                    "stage": f"Faylga {i}-qator yozilmoqda..."

                }
            )   

        return {
            "status": "Fayl yaratildi",
            "file_name": filename,
            "path_path": file_path
        }