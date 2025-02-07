import logging

import algokit_utils
import algokit_utils.application_client
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.control_flow.for_loops_example_client import (
    ForLoopsExampleClient,
)
from smart_contracts.artifacts.control_flow.if_else_example_client import (
    IfElseExampleClient,
)
from smart_contracts.artifacts.control_flow.match_statements_client import (
    MatchStatementsClient,
)
from smart_contracts.artifacts.control_flow.while_loop_example_client import (
    WhileLoopExampleClient,
)

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:

    app_clients = (
        ForLoopsExampleClient,
        MatchStatementsClient,
        WhileLoopExampleClient,
        IfElseExampleClient,
    )
    for client in app_clients:
        app_client = client(
            algod_client,
            creator=deployer,
            indexer_client=indexer_client,
        )
        app_client.deploy(
            on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
            on_update=algokit_utils.OnUpdate.AppendApp,
        )
