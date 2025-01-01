from dagster import ScheduleDefinition
from .jobs import movies_job

movies_schedule = ScheduleDefinition(
    name="movies_schedule",
    job=movies_job,
    cron_schedule="* * * * *",
)