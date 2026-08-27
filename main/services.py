from celery.result import AsyncResult
from config.celery import app as celery_app

READY_STATES= {"SUCCESS", "FAILURE","REVOKED"}

def build_task_status(task_id:str) ->dict:
    result = AsyncResult(task_id, app=celery_app)

    state = result.state
    payload={
        "task_id":task_id,
        "state": state,
        "ready": state in READY_STATES,
        "successful": True if state == "SUCCESS" else (
            False if state in {"FAILURE", "REVOKED"} else None
        ),

        "progress":None,
        "result": None,
        "error" : None,
                }

    if state == "PROGRESS" and isinstance(result.info, dict):
        current = result.info.get("current", 0)
        total = result.info.get("total", 1) or 1
        payload["progress"] = {
            "current": current,
            "total": total,
            "percent": round((current / total) * 100, 1),
            # "stage": result.info.get("stage", ""),
        }
    elif state == "SUCCESS":
        payload["result"] = result.result
        payload["progress"] = {"current": 100, "total": 100, "percent": 100.0}

        
    elif state == "FAILURE":
        exc = result.result
        payload["error"] = {
            "type": type(exc).__name__ ,#if exc else "Exception",
            "detail": str(exc),
        }
    return payload











