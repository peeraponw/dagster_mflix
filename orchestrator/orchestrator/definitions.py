from dagster import Definitions, load_assets_from_modules, EnvVar

from .assets import mongodb, movies
from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_snowflake import SnowflakeResource

mongodb_asset = load_assets_from_modules([mongodb])
movies_asset = load_assets_from_modules([movies], group_name="movies")

snowflake = SnowflakeResource(
    account=EnvVar("SNOWFLAKE_ACCOUNT"),
    user=EnvVar("SNOWFLAKE_USER"),
    password=EnvVar("SNOWFLAKE_PASSWORD"),
    role=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__ROLE"),
    database=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE"),
    warehouse=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE"),
    schema=EnvVar("mflix"),
)


defs = Definitions(
    assets=[*mongodb_asset, *movies_asset],
    resources={
        'dlt': DagsterDltResource(),
        'snowflake': snowflake
    }
)
