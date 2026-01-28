from celery import Celery
from app.config.setting import settings
# 配置消息代理 (Redis) 和 结果后端 (Redis)
celery_app = Celery(
    "rag_tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1"
)

# 任务配置，例如限制任务并发数
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=True,
)