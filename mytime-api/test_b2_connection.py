import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Backblaze B2 Connection...")
print("-" * 50)

try:
    # Get credentials from environment
    endpoint = os.getenv("B2_ENDPOINT", "s3.us-east-005.backblazeb2.com")
    key_id = os.getenv("B2_KEY_ID")
    app_key = os.getenv("B2_APP_KEY")
    bucket_name = os.getenv("B2_BUCKET_NAME")
    
    print(f"Endpoint: {endpoint}")
    print(f"Key ID: {key_id[:10]}..." if key_id else "Key ID: Not set")
    print(f"Bucket: {bucket_name}")
    
    # Initialize client
    client = boto3.client(
        's3',
        endpoint_url=f'https://{endpoint}',
        aws_access_key_id=key_id,
        aws_secret_access_key=app_key,
        config=Config(signature_version='s3v4')
    )
    
    # Test connection by listing buckets
    response = client.list_buckets()
    
    print("\n✅ SUCCESS! Connected to Backblaze B2")
    print(f"Account ID: {response.get('Owner', {}).get('ID', 'Unknown')}")
    print("\nBuckets:")
    for bucket in response.get('Buckets', []):
        print(f"  - {bucket['Name']}")
        
    # Test bucket access if bucket name is provided
    if bucket_name:
        try:
            objects = client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
            print(f"\nFiles in '{bucket_name}':")
            if 'Contents' in objects:
                for obj in objects['Contents']:
                    print(f"  - {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("  (empty bucket)")
        except Exception as e:
            print(f"\n⚠️  Cannot access bucket '{bucket_name}': {str(e)}")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure boto3 is installed: pip install boto3")
    
except Exception as e:
    print(f"❌ Connection Failed: {str(e)}")
    print("\nTroubleshooting tips:")
    print("1. Check your B2_KEY_ID and B2_APP_KEY in .env file")
    print("2. Verify the B2_ENDPOINT is correct")
    print("3. Make sure your IP is allowed in Backblaze CORS settings")