import os


broker_url = "redis://redis:6379/0" if os.getenv("DOCKER") else "redis://localhost:6379/0"
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Moscow"
enable_utc = True
