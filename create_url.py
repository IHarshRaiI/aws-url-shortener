import json
import uuid
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("url-shortener")


# Common CORS headers
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST",
    "Content-Type": "application/json"
}


def lambda_handler(event, context):
    try:
        # Body comes in as a JSON string
        body = json.loads(event.get("body") or "{}")
        long_url = body.get("long_url")

        if not long_url:
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Missing long_url parameter"})
            }

        # Generate 6-character short id
        short_id = uuid.uuid4().hex[:6]

        # Save to DynamoDB
        table.put_item(
            Item={
                "short_id": short_id,
                "long_url": long_url
            }
        )

        # Return short URL info
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "message": "URL shortened successfully",
                "short_id": short_id,
                "short_url": f"https://1uao0nf1sd.execute-api.us-east-1.amazonaws.com/prod/{short_id}"
            })
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }
