from dagster import Definitions, load_assets_from_modules, EnvVar, ExperimentalWarning

from .assets import mongodb, movies
from .resources import snowflake_resource, dlt_resource
from .jobs import movies_job
from .schedules import movies_schedule

import warnings
warnings.filterwarnings("ignore", category=ExperimentalWarning)


mongodb_asset = load_assets_from_modules([mongodb])
movies_asset = load_assets_from_modules([movies], group_name="movies")


defs = Definitions(
    assets=[*mongodb_asset, *movies_asset],
    resources={
        'dlt': dlt_resource,
        'snowflake': snowflake_resource
    },
    jobs=[movies_job],
    schedules=[movies_schedule]
)
