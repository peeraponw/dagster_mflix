from dagster import Definitions, load_assets_from_modules

from .assets import mongodb_asset
from dagster_embedded_elt.dlt import DagsterDltResource

all_assets = load_assets_from_modules([mongodb_asset])

defs = Definitions(
    assets=[*all_assets],
    resources={
        'dlt': DagsterDltResource
    }
)
