import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("ANTHROPIC_API_KEY")

print("=" * 60)
print("Testing Anthropic API Key")
print("=" * 60)

if not api_key:
    print("❌ ERROR: No API key found in .env file")
    exit(1)

print(f"✓ API Key loaded: {api_key[:20]}...{api_key[-4:]}")

try:
    # Create client
    client = Anthropic(api_key=api_key)
    print("✓ Client created")
    
    # Test API call
    print("\n🤖 Sending test message...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say 'Hello! Your API key works perfectly!' and nothing else."}
        ]
    )
    
    print(f"\n✅ SUCCESS!")
    print(f"Response: {message.content[0].text}")
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nMake sure:")
    print("1. You copied the FULL API key")
    print("2. The key is in .env file")
    print("3. No extra spaces or quotes")