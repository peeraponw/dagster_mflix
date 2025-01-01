from dagster_snowflake import SnowflakeResource
from dagster import asset

import os
import pandas as pd
import matplotlib.pyplot as plt


@asset(
        deps=['dlt_mongodb_comments', 'dlt_mongodb_embedded_movies']
)
def user_engagement(snowflake: SnowflakeResource) -> None:
    pass


@asset(
        deps=['dlt_mongodb_embedded_movies']
)
def top_movies_by_month(snowflake: SnowflakeResource) -> None:
    pass


@asset(
        deps=['user_engagement']
)
def top_movies_by_engagement(snowflake: SnowflakeResource) -> None:
    pass