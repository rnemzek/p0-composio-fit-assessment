from composio import Composio

# Initialize the client
composio = Composio(
    api_key='ak_NguOTc4AwH4s0Qu_KUQ7',
    toolkit_versions={"github", "20260227_00"}
#    toolkit_versions={"GITHUB_LIST_REPOSITORY_ISSUES", "20260227_00"}
)

# Execute the correct action slug
try:
    result = composio.tools.execute(
        version="20260227_00",
#        user_id="pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003",
        user_id="default",
        slug="GITHUB_LIST_REPOSITORY_ISSUES",
        arguments={
            "owner": "rnemzek_cintara",
            "repo": "rnemzek/streaming-service-search-engine", # Just the repo name
            "state": "open"
        }
    )

except Exception as e:
    print(f"Error: {e}")

if not result:
    result="\nResult is not defined"
#    print("\nResult is not defined")

print(result)
# version 20260227_00
# user_id pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003
# auth config id ac_PU7SE53uOZi_
# account_id="
# user_id="pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003"
# slug GITHUB
# user_id=pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003
