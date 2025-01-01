from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_snowflake import SnowflakeResource

from dagster import EnvVar


snowflake_resource = SnowflakeResource(
    account=EnvVar("SNOWFLAKE_ACCOUNT"),
    user=EnvVar("SNOWFLAKE_USER"),
    password=EnvVar("SNOWFLAKE_PASSWORD"),
    role=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__ROLE"),
    database=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE"),
    warehouse=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE"),
    schema=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__SCHEMA"),
)

dlt_resource = DagsterDltResource()