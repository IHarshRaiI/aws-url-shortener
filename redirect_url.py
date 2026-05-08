import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("url-shortener")

def lambda_handler(event, context):
    try:
        # Get short_id from path, e.g. /46cce9
        path_params = event.get("pathParameters") or {}
        short_id = path_params.get("short_id")

        if not short_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing short_id in path"})
            }

        # Look up in DynamoDB
        resp = table.get_item(Key={"short_id": short_id})
        item = resp.get("Item")

        if not item:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Short URL not found"})
            }

        long_url = item["long_url"]

        # Redirect to the original URL
        return {
            "statusCode": 302,
            "headers": {
                "Location": long_url
            },
            "body": ""
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
