# How to create AWS URL Shortener

## Contents
* [Step 1](#step-1)
* [Step 2](#step-2)
* [Step 3](#step-3)
* [Step 4](#step-4)
* [Step 5: Update the Invoke URL in Your Lambda Code](#step-5-update-the-invoke-url-in-your-lambda-code)
* [Step 6: Host the Frontend on Amazon S3](#step-6-host-the-frontend-on-amazon-s3)
* [Step 7: Test the Complete System](#step-7-test-the-complete-system)
* [Full Project Architecture (Summary)](#full-project-architecture-summary)

---

## Step 1
So, I am guessing you already have an account in AWS thinking of that I am proceeding to the main steps.

Before we talk about DynamoDB, we have to understand two simple concepts: a Database and The Cloud.

### Theory section 
**1. What is a Database?**
Imagine you run a massive library. You need a way to keep track of every book, who checked it out, and when it’s due back. If you wrote this on paper, it would take forever to find anything. A database is just a digital filing cabinet. It is a piece of software designed to store, organize, and quickly find massive amounts of digital information.

**2. What is "The Cloud" (and AWS)?**
In the old days, if you wanted a database, you had to buy a physical computer (a server), plug it in at your office, and keep it running 24/7.
"The Cloud" just means using someone else's computer over the internet. AWS (Amazon Web Services) is a huge branch of Amazon. They own massive warehouses full of incredibly powerful computers all over the world. Instead of buying your own computer, you rent a tiny bit of space on Amazon's computers.

**So, what is DynamoDB?**
DynamoDB is a specific type of digital filing cabinet (database) created and owned by Amazon (AWS).
Here is what makes it special and why people use it:

**1. It is "Serverless" (Zero Maintenance)**
* **What this means:** When you own a physical computer, you have to worry about the hard drive filling up, the power going out, or the computer crashing if too many people try to use it at once.
* **What DynamoDB does:** "Serverless" means Amazon handles everything in the background. You never have to install an update, plug in a wire, or worry about it crashing. If 10 people use your app, Amazon gives you a little bit of power. If 10 million people suddenly use your app, Amazon instantly gives you more power so it doesn't crash. You just put your data in, and they do the chores.

**2. It is "NoSQL" (Extremely Flexible)**
* **What this means:** Older databases (called SQL databases) are very strict. They act like an Excel spreadsheet. If you create a spreadsheet with columns for "First Name," "Last Name," and "Phone Number," every single row must follow those exact rules. If you suddenly want to add "Favourite Colour" to one person, you must change the entire spreadsheet for everyone.
* **What DynamoDB does:** "NoSQL" means it is completely flexible. Instead of a strict spreadsheet, it’s like a magical folder system. You can drop a tiny piece of paper into Folder A, and a 100-page book into Folder B. DynamoDB doesn't force you to follow a strict shape for your data. As long as you stick a clear name tag (a "key") on the folder, DynamoDB is happy.

**3. It is Blisteringly Fast**
* **What it does:** The main selling point of DynamoDB is speed. Whether you have 10 pieces of information stored inside it, or 10 billion pieces of information, it can usually find and hand you the exact piece of data you asked for in less than a single millisecond.

### Practical section 
Search Dynamo DB in AWS console once open you will see the option to create table.
1. Click Create Table.
2. **Table Name:** `url-shortner`
   *(you can name anything but will need to change things according to you will understand it some steps forwards) (Later, when you write the code for your app, your code will say, "Hey Amazon, go look inside the drawer named url-shortner." It just helps keep things organized if you ever build other apps later.)* 3. **Partition Key Name:** `short_id` (String)
   *(Think of the Partition Key as the exact, unique label on a specific file folder. Every single item you put into this database must have this label, and no two folders can have the exact same label.)*
4. Nothing else should be touched and scroll down and press create table.

---

## Step 2

### Theory section 
**1. What is AWS Lambda?**
* **The Full Form:** AWS (Amazon Web Services) Lambda
* **What it is:** If DynamoDB is our digital filing cabinet, Lambda is the worker or the brain of our app. It is where you write your actual computer code.
* **How it works (Serverless):** In the past, you had to keep a computer running 24 hours a day, 7 days a week, just in case someone clicked your link at 3:00 AM. Lambda is different. It is asleep 99% of the time. The exact millisecond a user clicks your short link, Lambda "wakes up," runs your code, figures out where the user needs to go, and instantly goes back to sleep. You only pay for the fraction of a second that it is awake.

**2. What is IAM?**
* **The Full Form:** IAM (Identity and Access Management)
* **What it is:** IAM is Amazon’s ultimate security guard. It handles all the rules about who (or what) is allowed to touch different parts of your AWS account.
* **Why it exists:** Amazon’s number one rule is "deny everything by default." If you create a Lambda worker, and you create a DynamoDB filing cabinet, they are strictly forbidden from talking to each other. They are locked in separate rooms. If your Lambda worker tries to open the DynamoDB filing cabinet to look up a link, IAM will block it and say, "Access Denied."

**3. What is an IAM Role and Specific Permissions?**
* **What it is:** An IAM Role is basically a VIP ID Badge.
* **What Specific Permissions are:** These are the exact rules written on the back of the ID badge. For example, you don't just give someone a badge that says "Do whatever you want." You give them a badge that specifically says, "You are allowed to Read and Write files, but ONLY inside the filing cabinet named url-shortner. You cannot touch anything else."

### Practical section 
1. Search IAM in the AWS. 
2. Once entered in IAM you will see the option to create roles.
3. You will see the option of use case in it service or use case. You shall select Lambda and then press next.
4. It redirects you to permission policies search Dynamo DB full access and select it and proceed next.
5. Then it opens the page Name, Review. **Role Name:** `LambdaFullAccess` (or whatever name you want) and then scroll down and press create role.
6. Search Lambda. Now that our security guard (IAM) has handed out the VIP badges, it is time to hire our workers. In this step, we are going to create two separate AWS Lambda functions.

Remember earlier when we said a Lambda function is basically a tiny, invisible worker that wakes up, does its job, and goes back to sleep? For our URL shortener to work properly, we need to hire two different workers with two completely different jobs.
Here is what they will do:

**Worker 1: The "Creator" (Creating the URL)**
* **The Job:** Saving new links.
* **How it works:** When you open your app and paste a massive, ugly website link that you want to shorten, this first worker wakes up. It randomly generates a tiny, unique code (like aB3x9). It then takes that tiny code and your massive link, walks over to our DynamoDB filing cabinet, drops them both inside a new folder, and immediately goes back to sleep.

**Worker 2: The "Fetcher" (Fetching the URL)**
* **The Job:** Redirecting people to the right place.
* **How it works:** Later, when a random person on the internet actually clicks your new short link, the second worker wakes up. It looks at the tiny code they clicked (aB3x9), rushes over to the DynamoDB filing cabinet, opens the exact folder labeled aB3x9, grabs the massive link hidden inside, and instantly throws the user to that destination.

**Why use two separate workers?** You might wonder why we don't just hire one worker to do both jobs. In cloud computing, it is best practice to keep jobs as small and focused as possible. By separating them, our app becomes much faster and less prone to breaking. One worker only ever has to worry about writing to the filing cabinet, and the other only ever has to worry about reading from it.

7. When you open the Lambda you will see the option to create Function.
8. When the create function opens **Function Name:** `create_url`. **Runtime:** Python 3.12.
   * Then click on change default execution role.
   * Select use existing role.
   * And selected `LambdaFullAccess` which we created.
   * Then click on create function.
   * You will be redirected to `create_url` below you will see code delete the default code.
   * Remember when I said you can name anything in DynamoDB then name which I put was `url-shortner` as you can check 5 line its searching for it so remember to put the name which you did.
   * And paste this code:

```python
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
                "short_url": f"[https://1uao0nf1sd.execute-api.us-east-1.amazonaws.com/prod/](https://1uao0nf1sd.execute-api.us-east-1.amazonaws.com/prod/){short_id}"
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
```

9. Now we will create one more functions in Lambda this will help fetching the url you will see on top right lambda>Functions> click on the function and then you will see the option to create the function again and click on it.
10. **Function Name:** `redirect_url`. **Runtime:** Python 3.12.
    * Then click on change default execution role.
    * Select use existing role.
    * And selected `LambdaFullAccess` which we created.
    * Then click on create function.
    * You will be redirected to `redirect_url` below you will see code delete the default code.
    * And paste this code:

```python
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
```

Remember this on `short_id` on the try code this name is important in upcoming step you can change it if you want.

---

## Step 3

### Theory section 
**What is API Gateway?**
* **The Full Form:** Amazon API (Application Programming Interface) Gateway
* **What it is:** Think of this as the Front Door or the Receptionist of your application.
* **What it does:** It provides a specific web address (a URL) that the public can actually click on. When someone visits that address, the API Gateway catches the request, checks if it’s valid, and then rings the doorbell of the correct Lambda worker to handle the job.

### Practical section 
1. You will search For now API Gateway.
2. Once you click on it you will see the option to create API click on it.
3. Then scroll down and chooses Rest API.

**First, what is an API?**
* **The Full Form:** Application Programming Interface.
* **What it is:** Think of an API as a Digital Menu. When you go to a restaurant, you don’t go into the kitchen and start cooking. You look at a menu, pick a dish, and the waiter (the API) tells the chef what to make. An API is just a set of rules that lets your website "order" data from your Lambda workers.

**What is a REST API?**
* **The Full Form:** REpresentational State Transfer API.
* **What it is:** This is the most popular "style" of menu in the world. It’s a standard way of organizing how computers talk to each other using simple web links.

**Why did we choose REST API instead of the others?**
Even though there are newer, "lighter" options, we choose the REST API for your guide.
* **1. The "Professional Toolkit" (Features):** The REST API is like a professional-grade toolbox. It comes with built-in features that help manage traffic, like API Keys (to make sure only your users can use it) and Request Validation (checking if the link someone sent is actually a real link before it even reaches your Lambda worker).
* **2. Fine-Grained Control:** In the REST API menu, you can control every tiny detail of how the "order" is placed and how the "food" (the data) is served back to the user. For a URL shortener, this control is great because it allows us to handle things like "Redirection" (automatically sending the user to the long URL) very smoothly.

4. Click on build. 
   * **API Name:** `url-shortener-api`
   * **Security policy:** `Securitypolicy_TLS13` in last (recommended)
   * Then just simply select create API.
5. It will redirect you to resources where path will be created as `/`.
6. While `/` is selected select resources above it it will redirect to create resource. Inside it resource name will be `{short_id}` and then press create resource. It will redirect to resources now you will also have `/{short_id}` (remember in the `redirect_url` code I mentioned `short_id` in the code you must change the code name if you change the name here) just reminder and same will happen with 2 resource.
7. Select `{short_id}` and right side you will see create method click on it.
   * **Method type:** GET 
   * **Lambda proxy integration** you will enable it.
   * **Lambda function:** You will select the `redirect_url` and scroll down and select create method.
8. Now we will create 2 resource click on `/` then click on create resource.
9. **Resource Name:** `shorten`. Then click on create resource you will be redirected to resource where you will see this:
   * `/`
   * `/{short_id}` GET
   * `/shorten`
10. While selecting `shorten` press create method.
    * **Method type** POST. 
    * Enable lambda proxy integration.
    * **Lambda function:** You will select the `create_url` and scroll down and select create method. You will see post being added below shorten.
11. On the left side below API Gateway you will see APIs select on it you will see `url-shortener-api` click on it then it will redirect you to resources then you will see deploy api right hand side active click on it.
12. **Stage:** You will select NEW STAGE. **Stage Name:** `prod` and then click deploy. It will redirect you to the stage page on the right side you will see stage detail below it you will see Invoke URl copy that.

**You can check if this works with the help of postman website:**
1. Once you login on the post man you need to select from the drop down Post put your invoke url in the end of the url you will see `/prod` add after it this `/shorten` : `prod/shorten`.
2. Now below the link you will see multiple name click on body.
3. You will see multiple name below after selecting body click on raw on the last you will JSON if not select the last option which will have drop down select JSON.
4. Now you will see you can type code:

```json
{
  "long_url": "[https://www.google.com](https://www.google.com)"
}
```

5. You can replace the `https://www.google.com` with any url you want then click on send.
6. Below you will see a message pop as message short id and short url just.
7. Copy the link infront of short URl and past it on new tab if it works your code is ready if it doesn’t then follow the next step if after following that step if its works good you learned something if doesn’t you are your on.

---

## Step 4
### Step 4: Enable CORS on API Gateway

**Theory: What is CORS?**
CORS stands for Cross-Origin Resource Sharing. It is a browser security rule that blocks your frontend webpage from making requests to a backend that lives on a different web address (domain).
Since your HTML page will be hosted on S3 (one address) and your API is on API Gateway (a completely different address), the browser will block all requests between them unless you explicitly tell API Gateway, "Yes, it is okay to accept requests from other origins."
Without CORS, your frontend button will silently fail — the code runs but nothing happens.

1. Go back to API Gateway in the AWS Console.
2. Select your `url-shortener-api`.
3. Click on the `/shorten` resource.
4. At the top, click **Enable CORS**.
5. Check the box for **POST** and also check **DEFAULT 4XX** and **DEFAULT 5XX**.
6. Click **Save**.
7. Now click on `/{short_id}` resource.
8. Click **Enable CORS** again.
9. Check **GET** and the default error boxes.
10. Click **Save**.
11. Once done, click **Deploy API** again → select the existing `prod` stage → click **Deploy**.

---

## Step 5: Update the Invoke URL in Your Lambda Code
Now that you have your Invoke URL (copied at the end of Step 3), you need to put it in your `create_url` Lambda code.

1. Go to Lambda → open `create_url`.
2. Find this line near the bottom of the code:

```python
"short_url": f"[https://1uao0nf1sd.execute-api.us-east-1.amazonaws.com/prod/](https://1uao0nf1sd.execute-api.us-east-1.amazonaws.com/prod/){short_id}"
```

Now here comes the issue when I told you if your postman doesn’t work is because that I gave you the code which had already invoke so yahe you need to replace it but it wont be that hard just copy the code above and search it in that code in `create_url` and yes I lied you are alone I am with you duhh.

3. Replace `https://1uao0nf1sd.execute-api.us-east-1.amazonaws.com/prod/` with your own Invoke URL followed by `/prod/` if it is not already there.
4. Click **Deploy** inside the Lambda code editor to save the change.

---

## Step 6: Host the Frontend on Amazon S3

**Theory: What is Amazon S3 for Hosting?**
S3 (Simple Storage Service) is normally used to store files. But AWS has a feature called Static Website Hosting that lets an S3 bucket serve your HTML file directly as a live webpage that anyone on the internet can open in their browser.
Think of it as putting your `index.html` file on Amazon's servers and giving it a public web address.

**Practical: Create the S3 Bucket**
1. Search for S3 in the AWS Console.
2. Click **Create bucket**.
3. **Bucket name:** `url-shortener-frontend` (must be globally unique — add random numbers if needed).
4. **Region:** Keep it the same as your Lambda and DynamoDB (e.g., `us-east-1`).
5. **Block Public Access:** Uncheck "Block all public access" and confirm the warning checkbox that appears below.
6. Leave everything else as default and click **Create bucket**.

**Practical: Enable Static Website Hosting**
1. Click on your new bucket to open it.
2. Go to the **Properties** tab.
3. Scroll all the way down to **Static website hosting**.
4. Click **Edit** → select **Enable**.
5. **Index document:** `index.html`
6. **Error document:** `error.html`
7. Click **Save changes**.
8. After saving, you will see a Bucket website endpoint URL — copy this, it is your live frontend address.

**Practical: Add a Bucket Policy (Make It Public)**
1. Go to the **Permissions** tab of your bucket.
2. Scroll to **Bucket Policy** → click **Edit**.
3. Paste this policy (replace `url-shortener-frontend` with your actual bucket name):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::url-shortener-frontend/*"
    }
  ]
}
```

4. Click **Save changes**.

**Practical: Create and Upload index.html**
1. Create a file named `index.html` on your computer and paste this code. Replace `YOUR_INVOKE_URL` with your actual API Gateway Invoke URL:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>URL Shortener</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 80px auto; padding: 20px; }
    input { width: 100%; padding: 10px; font-size: 16px; margin-bottom: 10px; box-sizing: border-box; }
    button { padding: 10px 20px; font-size: 16px; background: #ff9900; border: none; cursor: pointer; color: white; border-radius: 4px; }
    #result { margin-top: 20px; font-size: 16px; color: green; }
    #error { margin-top: 20px; font-size: 16px; color: red; }
  </style>
</head>
<body>
  <h1>URL Shortener</h1>
  <input type="text" id="longUrl" placeholder="Paste your long URL here..." />
  <button onclick="shortenUrl()">Shorten URL</button>
  <div id="result"></div>
  <div id="error"></div>

  <script>
    async function shortenUrl() {
      const longUrl = document.getElementById("longUrl").value.trim();
      document.getElementById("result").innerText = "";
      document.getElementById("error").innerText = "";

      if (!longUrl) {
        document.getElementById("error").innerText = "Please enter a URL.";
        return;
      }

      try {
        const response = await fetch("YOUR_INVOKE_URL/prod/shorten", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ long_url: longUrl })
        });

        const data = await response.json();

        if (response.ok) {
          document.getElementById("result").innerHTML =
            "Short URL: <a href='" + data.short_url + "' target='_blank'>" + data.short_url + "</a>";
        } else {
          document.getElementById("error").innerText = "Error: " + data.error;
        }
      } catch (err) {
        document.getElementById("error").innerText = "Request failed: " + err.message;
      }
    }
  </script>
</body>
</html>
```

2. Now upload it:
3. Go to your S3 bucket → click the **Objects** tab.
4. Click **Upload** → **Add files** → select your `index.html`.
5. Click **Upload**.

---

## Step 7: Test the Complete System
1. Open the Bucket website endpoint URL you copied earlier in your browser.
2. Paste any long URL (e.g., `https://www.youtube.com/watch?v=example`) into the input box.
3. Click **Shorten URL**.
4. You should see a short URL appear like `https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/ab3c9f`.
5. Copy that short URL, open it in a new browser tab — you should be automatically redirected to the original long URL.

---

## Full Project Architecture (Summary)
Here is how all 5 AWS services connect together in your finished project:

| Step | Service | Role |
| :--- | :--- | :--- |
| **User opens the app** | S3 | Serves the HTML frontend |
| **User clicks Shorten** | API Gateway `/shorten` POST | Receives the request |
| **Short ID is created** | Lambda `create_url` | Generates ID, stores in DB |
| **Data is saved** | DynamoDB `url-shortener` | Stores `short_id` → `long_url` |
| **User clicks short link** | API Gateway `/{short_id}` GET | Receives redirect request |
| **User is redirected** | Lambda `redirect_url` | Looks up DB, returns 302 |

If still this steps doesn’t work then I am sorry man I am still learning
If it works try the postman too 
