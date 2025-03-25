# from algokit_utils import ApplicationClient

# from algokit_utils_py_examples.helpers import setup_localnet_environment
# from smart_contracts.artifacts.reference_account_app.reference_account_app_client import (
#     ReferenceAccountAppClient,
# )


# def account_app_reference_example_method1():
#     # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_1

#     # Setup the test environment
#     env = setup_localnet_environment()
#     reference_account_app_app_client = env.reference_account_app_app_client

#     # Get the ReferenceAccountAppClient (implementation specific to your app)
#     reference_account_app_app_client = ApplicationClient(
#         client=algorand_client,
#         app_id=1,  # Example app ID
#         sender=account_a.address,
#         signer=account_a.signer,
#         app_spec=ReferenceAccountAppClient.app_spec,
#     )

#     # Configure automatic resource population per app call
#     result1 = reference_account_app_app_client.call(
#         method="get_my_counter",
#         args={},
#         populate_app_call_resources=True,
#     )

#     print("Method #1 My Counter", result1.return_value)

#     # Or set the default value for populate_app_call_resources to true globally and apply to all app calls
#     reference_account_app_app_client.populate_app_call_resources = True

#     result2 = reference_account_app_app_client.call(
#         method="get_my_counter",
#         args={},
#     )

#     print("Method #1 My Counter", result2.return_value)
#     # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_1


# def account_app_reference_example_method2():
#     # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_2

#     # Setup the test environment
#     algorand_client, _, account_a, _, _ = setup_localnet_environment()

#     # Get the ReferenceAccountAppClient (implementation specific to your app)
#     reference_account_app_app_client = ApplicationClient(
#         client=algorand_client,
#         app_id=1,  # Example app ID
#         sender=account_a.address,
#         signer=account_a.signer,
#         app_spec=ReferenceAccountAppClient.app_spec,
#     )

#     # Include the account and app references in the app call arguments to be populated automatically
#     result = reference_account_app_app_client.call(
#         method="get_my_counter_with_arg",
#         args={
#             "account": account_a.address,
#             "app": 1717,  # Using the default app ID from the contract
#         },
#     )

#     print("Method #2 My Counter", result.return_value)
#     # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_2


# def account_app_reference_example_method3():
#     # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_3

#     # Setup the test environment
#     algorand_client, _, account_a, _, _ = setup_localnet_environment()

#     # Get the ReferenceAccountAppClient (implementation specific to your app)
#     reference_account_app_app_client = ApplicationClient(
#         client=algorand_client,
#         app_id=1,  # Example app ID
#         sender=account_a.address,
#         signer=account_a.signer,
#         app_spec=ReferenceAccountAppClient.app_spec,
#     )

#     # Manually provide both account and app references in the respective arrays
#     result = reference_account_app_app_client.call(
#         method="get_my_counter",
#         args={},
#         account_references=[account_a.address],
#         app_references=[1717],  # Using the default app ID from the contract
#     )

#     print("Method #3 My Counter", result.return_value)
#     # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_3


# if __name__ == "__main__":
#     account_app_reference_example_method1()
#     account_app_reference_example_method2()
#     account_app_reference_example_method3()
