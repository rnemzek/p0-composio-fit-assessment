from composio import Composio

client = Composio(api_key="ak_NguOTc4AwH4s0Qu_KUQ7")

try:
    # In 0.11.x, initiate often takes the app name as the FIRST positional argument
    # and the user/entity ID as the second.
    connection = client.connected_accounts.initiate(
        "gmail", 
        entity_id="pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003"
    )
    print(f"\n--- LINK GMAIL HERE, BIG SEXY ---\n{connection.redirectUrl}\n")

except Exception as e:
    print(f"Positional failed: {e}")
    try:
        # Final Stand: Use the ToolSet helper if it exists in your path
        from composio import ComposioToolSet
        ts = ComposioToolSet(api_key="ak_NguOTc4AwH4s0Qu_KUQ7")
        # In some 0.11.1 sub-versions, it's back to 'app_name'
        conn = ts.connected_accounts.initiate(app_name="gmail", entity_id="pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003")
        print(f"ToolSet Success: {conn.redirectUrl}")
    except Exception as e2:
        print("\n❌ SDK confusion level 100. Let's do the 'Big Sexy' manual move:")
        print("1. Go to: https://app.composio.dev")
        print("2. Search for 'Gmail' and click 'Connect'.")
        print("3. When it asks for an ID, paste this: pg-test-fb03294d-998b-4fbd-8143-ab9f142e7003")
        print("4. Complete the Google sign-in.\n")

