STAGE 1 ✅
GitHub Repository
       ↓
GitHub Actions
       ↓
Failed Pipeline


STAGE 2
Python Agent
       ↓
GitHub API
       ↓
Fetch Failed Logs


STAGE 3
AI Analysis
       ↓
Analyze logs
       ↓
Identify root cause


STAGE 4
Troubleshooting Report
       ↓
Category
Root cause
Evidence
Recommendation
Confidence


STAGE 5
Agentic Workflow
       ↓
Suggest code change
       ↓
Create branch
       ↓
Create Pull Request
       ↓
Run CI again

########################################################
Great 👍 Stage 1 is done. Now let's build Stage 2: a Python agent that can read the failed GitHub Actions logs.

We'll keep this beginner-friendly. Don't worry about AI yet — first we'll make sure our Python program can talk to GitHub and retrieve the failure.

Stage 2 — Connect Python Agent to GitHub
Step 2.1 — Create a GitHub Personal Access Token

Your Python program needs permission to read your repository's Actions data.

Go to your GitHub account:

Profile picture → Settings → Developer settings → Personal access tokens → Tokens (classic)

Click Generate new token (classic).

Give it:

Name: ai-cicd-agent

Set an expiration, for example 30 days.

For permissions, select:

☑ repo

Then click Generate token.

⚠️ Copy the token immediately. GitHub won't show it again.

It will look roughly like:

ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Don't paste the token here or commit it into GitHub.

###################################################################

Step 2.2 — Create a local project

On your Mac, open Terminal.

Run:

mkdir ai-cicd-agent
cd ai-cicd-agent

Check:

pwd

You should see something like:

/Users/yourname/ai-cicd-agent
Step 2.3 — Create a Python virtual environment

Run:

python3 -m venv venv

Activate it:

source venv/bin/activate

You should now see something like:

(venv) yourname@Mac ai-cicd-agent %
Step 2.4 — Install the GitHub library

Run:

pip install PyGithub

Wait for it to finish.

Then:

pip show PyGithub

You should see information about the installed package.

Step 2.5 — Create our first Python program

Create a file:

touch agent.py

Open it in your editor.

If you're using VS Code:

code .

Then open:

agent.py

Put this code inside:

from github import Github

# Your GitHub Personal Access Token
GITHUB_TOKEN = "PASTE_YOUR_TOKEN_HERE"

# Your repository
REPOSITORY = "YOUR_GITHUB_USERNAME/ai-cicd-troubleshooter"


def main():

    print("Connecting to GitHub...")

    github = Github(GITHUB_TOKEN)

    repo = github.get_repo(REPOSITORY)

    print(f"Connected to repository: {repo.full_name}")

    print("\nRecent workflow runs:")

    runs = repo.get_workflow_runs()

    for run in runs[:5]:
        print(
            f"ID: {run.id} | "
            f"Name: {run.name} | "
            f"Status: {run.status} | "
            f"Conclusion: {run.conclusion}"
        )


if __name__ == "__main__":
    main()
Step 2.6 — Change two things

Find:

GITHUB_TOKEN = "PASTE_YOUR_TOKEN_HERE"

Replace it with your token:

GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxx"

Then find:

REPOSITORY = "YOUR_GITHUB_USERNAME/ai-cicd-troubleshooter"

For example, if your GitHub username is:

sahnawaj

change it to:

REPOSITORY = "sahnawaj/ai-cicd-troubleshooter"
Step 2.7 — Run the agent

In Terminal:

python agent.py

You should get something similar to:

Connecting to GitHub...

Connected to repository: sahnawaj/ai-cicd-troubleshooter

Recent workflow runs:

ID: 123456789 | Name: CI Pipeline | Status: completed | Conclusion: failure

🎉 That's our first connection between your AI agent and GitHub.

Your architecture now becomes:

                 GitHub
                   │
                   │ GitHub API
                   ▼
             ┌─────────────┐
             │ Python Agent│
             └─────────────┘
                   │
                   ▼
          Workflow Information
                   │
                   ▼
             ❌ FAILURE
             
             
             
             
🔐 Important: don't leave the token in agent.py

For this first test it's okay to understand how it works, but don't commit this file with your token to GitHub.

Once the connection works, we'll change it to use an environment variable:

GITHUB_TOKEN

so the secret isn't stored in your source code.

Next

After running:

python agent.py

you should see your failed CI Pipeline listed.

Send me the output (you can remove your username/token if present), and we'll do Step 2.8 — retrieve the actual failed job log. That's the important part for your troubleshooting agent.


Step 2.8 — Get the actual failed log

Now we're going to change the agent so it finds the latest failed pipeline and downloads its actual job logs.

1. Replace your agent.py

Replace everything in agent.py with this:

from github import Github, Auth

# GitHub Personal Access Token
GITHUB_TOKEN = "PASTE_YOUR_TOKEN_HERE"

# GitHub repository
REPOSITORY = "sahnawaj/ai-cicd-troubleshooter"


def main():

    print("Connecting to GitHub...")

    # New authentication syntax
    auth = Auth.Token(GITHUB_TOKEN)
    github = Github(auth=auth)

    repo = github.get_repo(REPOSITORY)

    print(f"Connected to repository: {repo.full_name}")

    print("\nSearching for failed workflow...")

    # Get workflow runs
    runs = repo.get_workflow_runs()

    failed_run = None

    for run in runs:

        if run.conclusion == "failure":
            failed_run = run
            break

    if failed_run is None:
        print("No failed workflow found.")
        return

    print("\nFailed workflow found!")
    print(f"Workflow: {failed_run.name}")
    print(f"Run ID: {failed_run.id}")
    print(f"Status: {failed_run.status}")
    print(f"Conclusion: {failed_run.conclusion}")
    print(f"URL: {failed_run.html_url}")

    # Get jobs belonging to this workflow run
    print("\nFetching jobs...")

    jobs = failed_run.jobs()

    for job in jobs:

        print("\n--------------------------------")
        print(f"Job: {job.name}")
        print(f"Status: {job.status}")
        print(f"Conclusion: {job.conclusion}")
        print("--------------------------------")

        # Print job steps
        for step in job.steps:

            print(
                f"Step: {step.name} | "
                f"Status: {step.status} | "
                f"Conclusion: {step.conclusion}"
            )


if __name__ == "__main__":
    main()
2. Important

Change:

GITHUB_TOKEN = "PASTE_YOUR_TOKEN_HERE"

to your existing token.

And make sure:

REPOSITORY = "sahnawaj/ai-cicd-troubleshooter"

matches your repository.


Step 2.9 — Run it

Run:

python agent.py

You should get something similar to:

Connecting to GitHub...

Connected to repository: sahnawaj/ai-cicd-troubleshooter

Searching for failed workflow...

Failed workflow found!

Workflow: CI Pipeline
Run ID: 33642078288
Status: completed
Conclusion: failure

Fetching jobs...

--------------------------------
Job: build-and-test
Status: completed
Conclusion: failure
--------------------------------

Step: Checkout code | Status: completed | Conclusion: success

Step: Setup Python | Status: completed | Conclusion: success

Step: Install dependencies | Status: completed | Conclusion: success

Step: Run application | Status: completed | Conclusion: failure

Step: Run tests | Status: completed | Conclusion: skipped

This is exactly what we want.

Your agent can now understand which step failed.




Excellent 👍 Stage 2.8 is working perfectly.

Your agent has now identified:

Workflow       → CI Pipeline
Run            → 33642078288
Job            → build-and-test
Failed step    → Run application
Tests          → skipped

Now let's get the actual failed log. This is the most important step before adding AI.

Step 2.9 — Download the failed job log
1. Install requests

You may already have it, but run:

pip install requests
2. Replace agent.py

Use this version:

from github import Github, Auth
import requests

# GitHub Personal Access Token
GITHUB_TOKEN = "PASTE_YOUR_TOKEN_HERE"

# GitHub repository
REPOSITORY = "sahnawaj/ai-cicd-troubleshooter"


def main():

    print("Connecting to GitHub...")

    # Authenticate with GitHub
    auth = Auth.Token(GITHUB_TOKEN)
    github = Github(auth=auth)

    # Connect to repository
    repo = github.get_repo(REPOSITORY)

    print(f"Connected to repository: {repo.full_name}")

    # --------------------------------------------------
    # 1. Find latest failed workflow
    # --------------------------------------------------

    print("\nSearching for failed workflow...")

    runs = repo.get_workflow_runs()

    failed_run = None

    for run in runs:

        if run.conclusion == "failure":
            failed_run = run
            break

    if failed_run is None:
        print("No failed workflow found.")
        return

    print("\nFailed workflow found!")
    print(f"Workflow: {failed_run.name}")
    print(f"Run ID: {failed_run.id}")
    print(f"URL: {failed_run.html_url}")

    # --------------------------------------------------
    # 2. Find failed job
    # --------------------------------------------------

    print("\nFetching jobs...")

    jobs = failed_run.jobs()

    failed_job = None

    for job in jobs:

        print(
            f"Job: {job.name} | "
            f"Status: {job.status} | "
            f"Conclusion: {job.conclusion}"
        )

        if job.conclusion == "failure":
            failed_job = job

    if failed_job is None:
        print("No failed job found.")
        return

    print("\nFailed job found!")
    print(f"Job name: {failed_job.name}")
    print(f"Job ID: {failed_job.id}")

    # --------------------------------------------------
    # 3. Download job log
    # --------------------------------------------------

    print("\nDownloading job log...")

    log_url = (
        f"https://api.github.com/repos/"
        f"{REPOSITORY}/actions/jobs/"
        f"{failed_job.id}/logs"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(
        log_url,
        headers=headers
    )

    if response.status_code != 200:

        print("Failed to download log.")
        print(f"HTTP status: {response.status_code}")
        print(response.text)

        return

    log = response.text

    # --------------------------------------------------
    # 4. Display log
    # --------------------------------------------------

    print("\n")
    print("=" * 70)
    print("FAILED JOB LOG")
    print("=" * 70)

    print(log)

    print("=" * 70)


if __name__ == "__main__":
    main()
Step 2.10 — Run it

Execute:

python agent.py

You should now see something similar to:

Connecting to GitHub...

Connected to repository: sahnawaj/ai-cicd-troubleshooter

Searching for failed workflow...

Failed workflow found!
Workflow: CI Pipeline
Run ID: 33642078288

Fetching jobs...

Job: build-and-test | Status: completed | Conclusion: failure

Failed job found!
Job name: build-and-test
Job ID: xxxxxxxxx

Downloading job log...

======================================================================
FAILED JOB LOG
======================================================================

...
Starting application...
Calculating total: price=100, quantity=5

Traceback (most recent call last):

  File ".../src/app.py", line ...

    total = (price * quantity) / discount

ZeroDivisionError: division by zero

Process completed with exit code 1.

======================================================================
🎯 What you've achieved

This is a significant milestone for your POC.

Your agent is now doing this autonomously:

             GitHub
                │
                ▼
        Find workflow runs
                │
                ▼
        Find failed run
                │
                ▼
          Find failed job
                │
                ▼
          Download logs
                │
                ▼
        ┌───────────────┐
        │ FAILED LOG    │
        │               │
        │ ZeroDivision  │
        │ Error         │
        └───────────────┘

And importantly, we haven't added AI yet.

That's intentional. We're separating the POC into:

1. CI data collection ✅
2. Log analysis ← we're here
3. AI reasoning
4. Recommendation
5. Automated remediation

Don't change anything else yet.

Run:

python agent.py

If you get the actual ZeroDivisionError log, send me the output (you can hide your token if it appears). Then we'll do Stage 3: add the AI model to analyze the log and produce a proper troubleshooting report.




Perfect. Stage 2.9 is successful. 🎉

Your agent has now retrieved the real GitHub Actions log, and the important failure is clearly:

ZeroDivisionError: division by zero

The uploaded output confirms the log retrieval worked.

We can now move to Stage 3 — AI Analysis.


#############################################################

Stage 3 — Let AI analyze the failed log

We'll make the agent take this:

GitHub Actions failed log
        ↓
       AI
        ↓
Troubleshooting Report

The report should eventually look like:

Pipeline Status: FAILED

Failure Category:
Application Error

Root Cause:
Division by zero in src/app.py

Failed File:
src/app.py

Failed Line:
5

Error:
ZeroDivisionError: division by zero

Explanation:
The application sets discount to 0 and then
attempts to divide by discount.

Recommended Fix:
Validate that discount is not zero before
performing the calculation.

Confidence:
99%
One important decision before we code

For the AI model, I recommend using the OpenAI API for this POC.

We'll set it up safely using:

OPENAI_API_KEY

rather than putting the key directly into your Python code.

The next steps will be:

Step 3.1  → Create OpenAI API key
Step 3.2  → Store it safely on your Mac
Step 3.3  → Install OpenAI Python SDK
Step 3.4  → Modify agent.py
Step 3.5  → Send failed log to AI
Step 3.6  → Get structured troubleshooting report

Don't change your GitHub pipeline now. It's doing exactly what we need.

If you're ready, I'll take you through Step 3.1, one command at a time.

Step 3.1 — OpenAI API key first. We'll keep this secure and simple.

Step 3.1 — Create an OpenAI API key

Go to the OpenAI API platform.

Sign in with your OpenAI account.
Open API keys.
Click Create new secret key.
Give it a name such as:
ai-cicd-troubleshooter
Create the key.
Copy it immediately.

It will look roughly like:

sk-xxxxxxxxxxxxxxxxxxxxxxxx

⚠️ Do not paste the key into this chat.
⚠️ Don't put it inside agent.py or commit it to GitHub.

Step 3.2 — Store the key on your Mac

You're currently in:

(venv) aafiyabiswas@Mac-6 ai-cicd-agent %

Run:

export OPENAI_API_KEY="YOUR_API_KEY_HERE"

Replace YOUR_API_KEY_HERE with your actual key.

For example:

export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"
Verify it exists

Run:

echo $OPENAI_API_KEY

You should see your key.

Don't send the output to me.


Step 3.3 — Install the OpenAI Python package

With your virtual environment still active:

pip install openai

Then verify:

pip show openai

You should see something like:

Name: openai
Version: ...

####################################################################
####################################################################
IMPORTANT NOTE - SINCE OPEN-AI API required some credit to purchase i am switching from OPEN AI API to Google AI
####################################################################
####################################################################

can i use gemini api 

Yes — Gemini API is a good choice for your POC, especially since your OpenAI API account currently has no credits.

Google's current Gemini API supports Python through the google-genai SDK, and Google AI Studio provides API keys. The free tier/limits depend on the model and current usage limits; paid usage requires billing.

For our project, we can simply replace the OpenAI part with Gemini.

Let's switch to Gemini

You're currently here:

(venv) ... ai-cicd-agent %
1. Get Gemini API key

Go to:

Google AI Studio

Create an API key.

Don't send the key to me.

2. Set the key

In your Terminal:

export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

Verify that it's set:

echo $GEMINI_API_KEY

Don't send me the output.

Google recommends using the GEMINI_API_KEY environment variable rather than putting the key directly in your Python code.

3. Install Gemini SDK

Run:

pip install -U google-genai

This is Google's current Python SDK; the older google-generativeai package is being superseded by google-genai.

4. Change test_ai.py

Replace its contents with:

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="Explain this CI error in one sentence: ZeroDivisionError: division by zero"
)

print(response.text)

Then run:

python test_ai.py

You should get something like:

The application attempted to divide a value by zero,
causing a ZeroDivisionError.
Then we're ready for the interesting part 🚀

Once this works, we'll modify your existing agent so it becomes:

GitHub
   ↓
Find failed workflow
   ↓
Find failed job
   ↓
Download job log
   ↓
Gemini
   ↓
Analyze failure
   ↓
┌──────────────────────────────┐
│ CI Troubleshooting Report    │
│                              │
│ Category: Application Error  │
│ Root Cause: Division by zero │
│ File: src/app.py             │
│ Line: 5                      │
│ Recommendation: ...          │
│ Confidence: 99%              │
└──────────────────────────────┘

Do the four steps above first. If python test_ai.py works, tell me "Gemini works", and we'll connect Gemini directly to the GitHub failure log you've already successfully retrieved.


Excellent! 🎉 Gemini is working.

The warning about automatic function calling isn't preventing anything — your request succeeded and Gemini returned the correct analysis.

Now let's combine the two things we've built:

GitHub Actions
      ↓
Failed Pipeline
      ↓
Python Agent
      ↓
Fetch Failed Job Log
      ↓
Gemini AI
      ↓
Troubleshooting Report
Stage 3.2 — Connect Gemini to your GitHub log

We'll modify agent.py so you no longer have to manually give the error to Gemini.

Replace agent.py with this
from github import Github, Auth
from google import genai
import requests
import os


# --------------------------------------------------
# Configuration
# --------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

REPOSITORY = "sahnawaj/ai-cicd-troubleshooter"


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # --------------------------------------------------
    # 1. Validate configuration
    # --------------------------------------------------

    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN is not set.")
        return

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY is not set.")
        return


    # --------------------------------------------------
    # 2. Connect to GitHub
    # --------------------------------------------------

    print("Connecting to GitHub...")

    auth = Auth.Token(GITHUB_TOKEN)
    github = Github(auth=auth)

    repo = github.get_repo(REPOSITORY)

    print(f"Connected to repository: {repo.full_name}")


    # --------------------------------------------------
    # 3. Find latest failed workflow
    # --------------------------------------------------

    print("\nSearching for failed workflow...")

    runs = repo.get_workflow_runs()

    failed_run = None

    for run in runs:

        if run.conclusion == "failure":
            failed_run = run
            break

    if failed_run is None:
        print("No failed workflow found.")
        return


    print("\nFailed workflow found!")
    print(f"Workflow: {failed_run.name}")
    print(f"Run ID: {failed_run.id}")
    print(f"URL: {failed_run.html_url}")


    # --------------------------------------------------
    # 4. Find failed job
    # --------------------------------------------------

    print("\nFetching jobs...")

    jobs = failed_run.jobs()

    failed_job = None

    for job in jobs:

        print(
            f"Job: {job.name} | "
            f"Status: {job.status} | "
            f"Conclusion: {job.conclusion}"
        )

        if job.conclusion == "failure":
            failed_job = job
            break

    if failed_job is None:
        print("No failed job found.")
        return


    print("\nFailed job found!")
    print(f"Job name: {failed_job.name}")
    print(f"Job ID: {failed_job.id}")


    # --------------------------------------------------
    # 5. Download failed job log
    # --------------------------------------------------

    print("\nDownloading job log...")

    log_url = (
        f"https://api.github.com/repos/"
        f"{REPOSITORY}/actions/jobs/"
        f"{failed_job.id}/logs"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(
        log_url,
        headers=headers
    )

    if response.status_code != 200:

        print("Failed to download log.")
        print(f"HTTP status: {response.status_code}")

        return

    log = response.text


    # --------------------------------------------------
    # 6. Send log to Gemini
    # --------------------------------------------------

    print("\nSending log to Gemini AI...")

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    prompt = f"""
You are an expert CI/CD troubleshooting engineer.

Analyze the following GitHub Actions failure log.

Identify:

1. Failure category
2. Root cause
3. Failed file
4. Failed line if available
5. Error message
6. Explanation
7. Recommended fix
8. Confidence score from 0 to 100

Be concise and only use evidence from the log.

GitHub Actions Log:

---------------- LOG START ----------------

{log}

---------------- LOG END ----------------
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )


    # --------------------------------------------------
    # 7. Display AI analysis
    # --------------------------------------------------

    print("\n")
    print("=" * 70)
    print("AI TROUBLESHOOTING REPORT")
    print("=" * 70)

    print(response.text)

    print("=" * 70)


if __name__ == "__main__":
    main()
One important change

Notice that we're no longer putting your GitHub token directly in the code:

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

That's much safer.

Step 3.3 — Set your GitHub token

You already have the GitHub token from earlier.

In your Terminal run:

export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"

For example:

export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"

You don't need to send it to me.

You should already have:

export GEMINI_API_KEY="YOUR_GEMINI_KEY"

So your current Terminal session has:

GITHUB_TOKEN
     ↓
GitHub access

GEMINI_API_KEY
     ↓
Gemini access
Step 3.4 — Run the complete agent 🚀

Now run:

python agent.py

This time you should see:

Connecting to GitHub...

Connected to repository: sahnawaj/ai-cicd-troubleshooter

Searching for failed workflow...

Failed workflow found!

Workflow: CI Pipeline
Run ID: 33642078288

Fetching jobs...

Job: build-and-test | Status: completed | Conclusion: failure

Failed job found!

Job name: build-and-test
Job ID: 100287404915

Downloading job log...

Sending log to Gemini AI...

And then something similar to:

======================================================================
AI TROUBLESHOOTING REPORT
======================================================================

Failure Category:
Application Error

Root Cause:
The application attempts to divide by zero.

Failed File:
src/app.py

Failed Line:
5

Error:
ZeroDivisionError: division by zero

Explanation:
The variable `discount` is set to 0 and is used
as the denominator in the calculation.

Recommended Fix:
Ensure discount is greater than zero before
performing the division.

Confidence:
99%

======================================================================
🎯 This is our first real AI-powered troubleshooting agent

You have gone from:

❌ GitHub pipeline

to:

❌ Pipeline
      ↓
📋 Logs
      ↓
🤖 Gemini
      ↓
🔍 Root Cause
      ↓
💡 Recommended Fix

That's already a legitimate small agentic-AI POC.

One thing I want to improve next

Right now we're sending the entire GitHub log to Gemini. Real CI logs can be thousands of lines long.

Next we'll add a Log Analyzer/Extractor that identifies the relevant failure section first:

10,000 line log
      ↓
Log Parser
      ↓
Relevant error ~20 lines
      ↓
Gemini
      ↓
Accurate diagnosis

After that, we can make it much more impressive by adding automatic fix generation and Pull Request creation.

Run the new agent.py first. If you get the AI TROUBLESHOOTING REPORT, send me the output and we'll proceed to the next stage.


Excellent! 🎉 Stage 3 is working.

You now have a functioning end-to-end pipeline:

GitHub Actions
      ↓
❌ Failed Pipeline
      ↓
Python Agent
      ↓
GitHub API
      ↓
Failed Job Log
      ↓
Gemini
      ↓
🤖 Troubleshooting Report

And Gemini correctly identified the actual root cause from your log.

The AFC message is only a warning, not a failure. We can ignore it for now.

Stage 4 — Make the agent smarter

Before we add automatic code fixing, I'd make one important improvement.

Currently we're sending the entire GitHub Actions log to Gemini. Your current log is already fairly large, and real-world CI logs can contain thousands or millions of characters.

Instead, we'll build:

10,000-line CI log
       ↓
   Log Analyzer
       ↓
Extract relevant failure
       ↓
     Gemini
       ↓
Structured diagnosis
What we'll add

The agent will automatically look for things such as:

ERROR
Error
Exception
Traceback
failed
FAIL
exit code

and extract the surrounding lines.

For your current failure, instead of sending the entire runner output, it should extract something approximately like:

Run python src/app.py

Starting application...
Calculating total: price=100, quantity=5

Traceback (most recent call last):

File ".../src/app.py", line 17
    total = calculate_total(price, quantity)

File ".../src/app.py", line 5
    total = (price * quantity) / discount

ZeroDivisionError: division by zero

Process completed with exit code 1.

Then Gemini analyzes only that relevant section.

But there's an even better improvement

For your POC, I'd like us to make Gemini return JSON, rather than free-form text.

Instead of:

1. Failure category...
2. Root cause...
3. Failed file...

we'll get:

{
  "failure_category": "Application Runtime Error",
  "root_cause": "Division by zero",
  "failed_file": "src/app.py",
  "failed_line": 5,
  "error": "ZeroDivisionError: division by zero",
  "explanation": "The discount value is zero...",
  "recommended_fix": "Validate discount before division",
  "confidence": 100
}

That is much more useful because your agent can make decisions based on the result.

For example:

                    Gemini
                       │
                       ▼
              Structured JSON
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Human Report        Auto-Fix Agent
                                   │
                                   ▼
                              Modify Code
                                   │
                                   ▼
                             Create Branch
                                   │
                                   ▼
                            Create PR
                                   │
                                   ▼
                           Run Pipeline
                                   │
                         ┌─────────┴─────────┐
                         ▼                   ▼
                       PASS                FAIL
                         │                   │
                         ▼                   ▼
                     Complete          Analyze Again

This is where your POC starts becoming genuinely agentic rather than just "AI summarizes a log."

I suggest we do this next:

Stage 4.1 → Extract relevant failure log
Stage 4.2 → Ask Gemini for structured JSON
Stage 4.3 → Display a clean troubleshooting report
Stage 4.4 → Add a second failure type to prove the agent generalizes
Stage 5 → Automatic fix + GitHub PR

We'll do it one step at a time, just like we've been doing.


Great. Let's do Stage 4.1 — extract only the useful part of the CI log.

This is an important improvement because we don't want to send the entire GitHub runner log to Gemini.

Step 4.1 — Add a log extractor

Open your agent.py.

Find this line:

log = response.text

Immediately after it, add:

# --------------------------------------------------
# Extract relevant failure information
# --------------------------------------------------

def extract_failure(log):

    lines = log.splitlines()

    # Keywords that commonly indicate failures
    error_keywords = [
        "Traceback",
        "Error:",
        "Exception:",
        "ERROR",
        "FAILED",
        "failure",
        "exit code"
    ]

    failure_lines = []

    for i, line in enumerate(lines):

        if any(keyword in line for keyword in error_keywords):

            # Include a few lines before and after the error
            start = max(0, i - 5)
            end = min(len(lines), i + 6)

            failure_lines.extend(lines[start:end])

    # Remove duplicates while preserving order
    unique_lines = list(dict.fromkeys(failure_lines))

    return "\n".join(unique_lines)

Then immediately after that, add:

relevant_log = extract_failure(log)

print("\n")
print("=" * 70)
print("EXTRACTED FAILURE LOG")
print("=" * 70)

print(relevant_log)

print("=" * 70)
Step 4.2 — Use the extracted log with Gemini

Now find this part in your code:

{log}

---------------- LOG END ----------------
"""

Change it to:

{relevant_log}

---------------- LOG END ----------------
"""

So Gemini will now receive:

GitHub full log
      ↓
extract_failure()
      ↓
Relevant failure
      ↓
Gemini
Step 4.3 — Run it

Save agent.py and run:

python agent.py

You should see something like:

Downloading job log...

======================================================================
EXTRACTED FAILURE LOG
======================================================================

Run python src/app.py

Starting application...
Calculating total: price=100, quantity=5

Traceback (most recent call last):

File ".../src/app.py", line 17

File ".../src/app.py", line 5

ZeroDivisionError: division by zero

Process completed with exit code 1.

======================================================================

Sending log to Gemini AI...

The exact extracted lines may be slightly different because we're using keyword matching.

Why we're doing this

Your current GitHub log contains lots of irrelevant information:

Runner version
Operating system
Git checkout
Python installation
pip installation
Node warnings
Environment variables
...

We don't need to send all of that to the AI.

We want:

                    FULL LOG
                       │
                       ▼
                ┌──────────────┐
                │ Log Analyzer │
                └──────────────┘
                       │
                       ▼
              Relevant Error
                       │
                       ▼
                    Gemini

This gives us a cleaner and more scalable architecture.

Don't worry about the code being perfect yet

We're building this incrementally:

Stage 1 ✅ GitHub pipeline failure
Stage 2 ✅ Python → GitHub → logs
Stage 3 ✅ Logs → Gemini → diagnosis
Stage 4.1 ← We are here
Stage 4.2 → Structured JSON response
Stage 4.3 → Clean troubleshooting report
Stage 4.4 → Test a different failure
Stage 5 → Automatic fix + Pull Request

Run it once and send me the EXTRACTED FAILURE LOG section. Then we'll do Stage 4.2 — structured JSON, which is where the agent becomes much more useful.

Perfect. Stage 4.1 is working exactly as intended. ✅

Your extractor successfully isolated the important failure:

src/app.py, line 5
total = (price * quantity) / discount

ZeroDivisionError: division by zero

It also shows something important for a real troubleshooting agent: the log contains an irrelevant Node 20 deprecation warning, while the actual pipeline failure is the Python exception. Our AI correctly ignored the warning.

Now let's make the output machine-readable.

Stage 4.2 — Gemini returns structured JSON

Currently Gemini gives us:

1. Failure category...
2. Root cause...
3. Failed file...

That's good for a human, but not ideal for an agent.

We want:

{
  "failure_category": "Application Runtime Error",
  "root_cause": "Division by zero",
  "failed_file": "src/app.py",
  "failed_line": 5,
  "error_message": "ZeroDivisionError: division by zero",
  "explanation": "...",
  "recommended_fix": "...",
  "confidence": 100
}

Then our Python program can actually use those fields.

Step 4.2.1 — Modify the Gemini section

Open agent.py.

Find this:

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt
)

Replace it with:

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json"
    }
)

This tells Gemini:

"Return JSON, not normal conversational text."

Step 4.2.2 — Change the prompt

Find your current prompt:

prompt = f"""
You are an expert CI/CD troubleshooting engineer.

Analyze the following GitHub Actions failure.

Identify:

1. Failure category
2. Root cause
3. Failed file
4. Failed line if available
5. Error message
6. Explanation
7. Recommended fix
8. Confidence score from 0 to 100

Only use evidence from the supplied log.

GitHub Actions failure log:

---------------- LOG START ----------------

{relevant_log}

---------------- LOG END ----------------
"""

Replace it with:

prompt = f"""
You are an expert CI/CD troubleshooting engineer.

Analyze the following GitHub Actions failure log.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "failure_category": "",
    "root_cause": "",
    "failed_file": "",
    "failed_line": null,
    "error_message": "",
    "explanation": "",
    "recommended_fix": "",
    "confidence": 0
}}

Rules:

- failure_category should describe the type of CI/CD failure.
- root_cause should identify the actual technical cause.
- failed_file should contain only the repository-relative file path if available.
- failed_line should be a number if available, otherwise null.
- error_message should contain the primary error.
- explanation should briefly explain why the failure occurred.
- recommended_fix should provide a practical fix.
- confidence should be a number between 0 and 100.
- Ignore unrelated warnings unless they caused the failure.
- Only use evidence from the supplied log.
- Do not include Markdown.
- Do not include ```json.
- Return JSON only.

GitHub Actions failure log:

---------------- LOG START ----------------

{relevant_log}

---------------- LOG END ----------------
"""
Step 4.2.3 — Parse the JSON

At the top of your file, add:

import json

So your imports become:

from github import Github, Auth
from google import genai
import requests
import os
import json

Now find:

print(response.text)

Replace it with:

# Parse Gemini response as JSON
analysis = json.loads(response.text)

print(f"Failure Category : {analysis['failure_category']}")
print(f"Root Cause       : {analysis['root_cause']}")
print(f"Failed File      : {analysis['failed_file']}")
print(f"Failed Line      : {analysis['failed_line']}")
print(f"Error Message    : {analysis['error_message']}")
print(f"Explanation      : {analysis['explanation']}")
print(f"Recommended Fix  : {analysis['recommended_fix']}")
print(f"Confidence       : {analysis['confidence']}%")
Step 4.2.4 — Run it

Save the file and run:

python agent.py

You should get something similar to:

======================================================================
AI TROUBLESHOOTING REPORT
======================================================================

Failure Category : Application Runtime Error
Root Cause       : Division by zero
Failed File      : src/app.py
Failed Line      : 5
Error Message    : ZeroDivisionError: division by zero

Explanation      : The calculate_total function attempts to divide
                   by a discount value of zero.

Recommended Fix  : Validate that discount is not zero before
                   performing the division.

Confidence       : 100%

======================================================================
Why this is a big step

Now your agent isn't simply asking Gemini:

"What do you think about this log?"

It is asking Gemini to produce a structured diagnosis that the program can consume.

That gives us this architecture:

                 GitHub
                   │
                   ▼
            Failed Workflow
                   │
                   ▼
             Failed Job
                   │
                   ▼
               Full Log
                   │
                   ▼
             Log Extractor
                   │
                   ▼
          Relevant Failure Log
                   │
                   ▼
                Gemini
                   │
                   ▼
            Structured JSON
                   │
          ┌────────┴─────────┐
          ▼                  ▼
     Human Report       Agent Decision
                              │
                              ▼
                         Auto Fix
And now we're approaching the interesting part 🚀

Once this works, Stage 4.3 will make the agent handle different failure types.

We'll deliberately introduce a second failure, for example:

ModuleNotFoundError

instead of:

ZeroDivisionError

and see whether the same agent automatically identifies:

Category: Dependency Error
Root Cause: Missing Python module
Fix: Install/add dependency

That will demonstrate that this isn't just hard-coded for your current error.

Run python agent.py now. If the structured report appears correctly, we'll move to the second failure scenario.


Perfect. ✅ Stage 4.2 is working.

This is now a proper machine-readable troubleshooting result:

GitHub failure
      ↓
Log extraction
      ↓
Gemini
      ↓
Structured JSON
      ↓
Diagnosis

And the agent correctly identified the real failure rather than the unrelated Node deprecation warning.

One small observation

The Gemini AFC message is still only a warning. Since the response is working correctly, we can leave it alone for now.


Stage 4.3 — Prove the agent works with another failure

This is important for your POC.

Right now someone could say:

"You just programmed the agent to recognize ZeroDivisionError."

We want to demonstrate that the agent can analyze different CI failures without changing the AI logic.

Let's create a dependency failure.

Step 4.3.1 — Change src/app.py

Go to your GitHub repository:

src/app.py

Replace the contents with:

import pandas


def process_data():
    data = pandas.DataFrame({
        "name": ["Alice", "Bob"],
        "score": [90, 85]
    })

    print(data)


if __name__ == "__main__":
    print("Starting application...")
    process_data()

Notice that we're importing:

import pandas

but our GitHub Actions pipeline currently installs only:

pip install pytest

So pandas isn't installed.

Step 4.3.2 — Commit the change

In GitHub:

Commit changes

Your pipeline should automatically start again.

Go to:

Actions → CI Pipeline

You should now see a new run.

Wait for it to finish.

It should fail with something similar to:

ModuleNotFoundError: No module named 'pandas'
Step 4.3.3 — Run your agent

Back in Terminal:

python agent.py

Your agent should automatically find the latest failed workflow and send the new failure to Gemini.

You should get something like:

======================================================================
AI TROUBLESHOOTING REPORT
======================================================================

Failure Category : Dependency Error

Root Cause       : The pandas Python package is not installed.

Failed File      : src/app.py

Failed Line      : 1

Error Message    : ModuleNotFoundError: No module named 'pandas'

Explanation      : The application imports pandas, but the CI
                   workflow does not install the pandas dependency.

Recommended Fix  : Add pandas to the dependency installation
                   step or requirements.txt.

Confidence       : 99%

======================================================================
🚀 This is a very important demonstration

Your same Python agent will now handle:

Failure #1
ZeroDivisionError
        ↓
Application Runtime Error
        ↓
Fix application logic

and:

Failure #2
ModuleNotFoundError
        ↓
Dependency Error
        ↓
Install pandas

No change to the AI prompt or troubleshooting logic.

That's much stronger evidence for your POC.

After that, we'll do something even better

Once you've demonstrated those two failures, we'll move toward the real agentic behavior:

             GitHub Actions
                    │
                    ▼
                 FAILED
                    │
                    ▼
              AI Agent
                    │
             Analyze failure
                    │
                    ▼
              Root Cause
                    │
                    ▼
             Generate Fix
                    │
                    ▼
          ┌─────────────────┐
          │ Human Approval? │
          └────────┬────────┘
                   │
                   ▼
             Create Branch
                   │
                   ▼
             Modify Code
                   │
                   ▼
             Create PR
                   │
                   ▼
             GitHub Actions
                   │
             ┌─────┴─────┐
             ▼           ▼
           PASS         FAIL
             │           │
             ▼           ▼
          Done      Analyze Again

That final loop is what will make your AI-powered CI/CD troubleshooting POC genuinely interesting.

For now, make the pandas change, let GitHub Actions fail, then run python agent.py. Send me the resulting report and we'll continue.

###################OUTPUT###########################
======================================================================

Sending log to Gemini AI...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.


======================================================================
AI TROUBLESHOOTING REPORT
======================================================================
Failure Category : Missing Dependency
Root Cause       : The Python module 'pandas' is not installed in the CI environment.
Failed File      : src/app.py
Failed Line      : 22
Error Message    : ModuleNotFoundError: No module named 'pandas'
Explanation      : Execution of src/app.py failed at line 22 because it attempted to import 'pandas', which was not installed in the Python environment.
Recommended Fix  : Add 'pandas' to your requirements file or install it via 'pip install pandas' prior to executing the Python script in your CI workflow.
Confidence       : 100%
======================================================================
######################################################################

Excellent. 🎉 Your agent has now demonstrated that it can generalize across different failure types.

You tested:

Scenario    AI diagnosis    Result
ZeroDivisionError    Runtime/Application error    ✅
ModuleNotFoundError    Missing dependency    ✅

And importantly, you didn't change the troubleshooting logic between the two tests.

That gives you a solid Stage 4 POC.

Next: Stage 5 — Make it actually agentic

Right now your workflow is:

GitHub
   ↓
Failed Pipeline
   ↓
Python Agent
   ↓
Extract Log
   ↓
Gemini
   ↓
Diagnosis

The next step is to have the AI propose a concrete code/configuration change, rather than just telling you what is wrong.

I'd suggest we do this safely in two stages:

Stage 5A
AI analyzes failure
       ↓
AI generates proposed fix
       ↓
Show proposed fix to user
       ↓
User approves

Then:

Stage 5B
Approved
   ↓
Create Git branch
   ↓
Apply fix
   ↓
Commit
   ↓
Create Pull Request
   ↓
GitHub Actions runs

And eventually:

              ┌──────────────┐
              │ GitHub CI    │
              └──────┬───────┘
                     │
                  FAILURE
                     ↓
             ┌──────────────┐
             │ AI Agent     │
             └──────┬───────┘
                    ↓
               Analyze
                    ↓
             Generate Fix
                    ↓
              Create PR
                    ↓
              CI runs again
                 /     \
              PASS      FAIL
               ↓         ↓
             Done    Analyze Again
             

Let's start with Stage 5A

We'll not allow the agent to modify your GitHub repository yet.

Instead, Gemini will return:

{
  "failure_category": "Missing Dependency",
  "root_cause": "pandas is not installed",
  "recommended_fix": "Add pandas to dependencies",
  "fix_type": "workflow",
  "proposed_changes": [
    {
      "file": ".github/workflows/ci.yml",
      "change": "Add pandas to pip install"
    }
  ]
}

Then your agent can display:

🤖 PROPOSED FIX

Problem:
pandas is missing from CI environment.

File:
.github/workflows/ci.yml

Change:
pip install pytest pandas

Confidence:
100%

⚠️ No changes have been made.

This human-in-the-loop approach is much safer and is also a better architecture to demonstrate in a POC.

One thing before we continue

Your current code has the Gemini model name:

model="gemini-3.7-flash"

Since you're successfully getting responses, leave it as-is for now.

Next we'll modify the JSON schema/prompt so Gemini produces both diagnosis + proposed remediation.

###
Great. Let's implement Stage 5A — AI-generated remediation, but keep it human-approved. We won't let the agent change GitHub yet.

Step 5A.1 — Update the Gemini prompt

In agent.py, find your current prompt and replace it with this:

prompt = f"""
You are an expert CI/CD troubleshooting engineer.

Analyze the following GitHub Actions failure log.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "failure_category": "",
    "root_cause": "",
    "failed_file": "",
    "failed_line": null,
    "error_message": "",
    "explanation": "",
    "recommended_fix": "",
    "confidence": 0,
    "fix_type": "",
    "proposed_changes": [
        {{
            "file": "",
            "change": ""
        }}
    ]
}}

Rules:

- failure_category: type of CI/CD failure.
- root_cause: actual technical cause.
- failed_file: repository-relative path if available.
- failed_line: line number if available, otherwise null.
- error_message: primary error.
- explanation: brief explanation of why it failed.
- recommended_fix: practical remediation.
- confidence: number from 0 to 100.
- fix_type: one of:
    - code
    - dependency
    - configuration
    - workflow
    - environment
    - unknown

- proposed_changes: list of concrete changes that could fix the failure.
- Each proposed change must contain:
    - file: repository-relative file path
    - change: specific modification to make

Important:

- Do NOT make any changes yourself.
- Do NOT assume files that are not supported by the log.
- Ignore unrelated warnings unless they caused the failure.
- Only use evidence from the supplied log.
- Return JSON only.
- Do not use Markdown.
- Do not include ```json.

GitHub Actions failure log:

---------------- LOG START ----------------

{relevant_log}

---------------- LOG END ----------------
"""
Step 5A.2 — Run the agent

Run:

python agent.py

Because your current GitHub failure is the missing pandas dependency, Gemini should produce something similar to:

======================================================================
AI TROUBLESHOOTING REPORT
======================================================================

Failure Category : Missing Dependency

Root Cause       : pandas is not installed in the CI environment.

Failed File      : src/app.py

Failed Line      : 1

Error Message    : ModuleNotFoundError: No module named 'pandas'

Explanation      : The application imports pandas but the CI workflow
                   does not install the package.

Recommended Fix : Add pandas to the CI dependencies.

Confidence       : 100%

Fix Type         : dependency

Proposed Changes:

File:
.github/workflows/ci.yml

Change:
Add pandas to the pip install command.

======================================================================
Step 5A.3 — Make Python display the proposed changes

Your current output code probably looks like this:

print(f"Failure Category : {analysis['failure_category']}")
print(f"Root Cause       : {analysis['root_cause']}")
print(f"Failed File      : {analysis['failed_file']}")
print(f"Failed Line      : {analysis['failed_line']}")
print(f"Error Message    : {analysis['error_message']}")
print(f"Explanation      : {analysis['explanation']}")
print(f"Recommended Fix  : {analysis['recommended_fix']}")
print(f"Confidence       : {analysis['confidence']}%")

Replace it with:

print(f"Failure Category : {analysis['failure_category']}")
print(f"Root Cause       : {analysis['root_cause']}")
print(f"Failed File      : {analysis['failed_file']}")
print(f"Failed Line      : {analysis['failed_line']}")
print(f"Error Message    : {analysis['error_message']}")
print(f"Explanation      : {analysis['explanation']}")
print(f"Recommended Fix  : {analysis['recommended_fix']}")
print(f"Confidence       : {analysis['confidence']}%")
print(f"Fix Type         : {analysis['fix_type']}")

print("\nProposed Changes:")

for change in analysis["proposed_changes"]:

    print(f"\nFile   : {change['file']}")
    print(f"Change : {change['change']}")
Step 5A.4 — Test it

Run:

python agent.py

Your output should now contain:

AI TROUBLESHOOTING REPORT

Failure Category : Missing Dependency

Root Cause       : The Python module 'pandas' is not installed.

...

Fix Type         : dependency

Proposed Changes:

File   : .github/workflows/ci.yml

Change : Add pandas to the pip install command.
🎯 What's different now?

Previously:

AI
 ↓
"What went wrong?"
 ↓
Answer

Now:

AI
 ↓
"What went wrong?"
 ↓
"How can it be fixed?"
 ↓
"Which file needs changing?"
 ↓
"What change should be made?"

But the agent still doesn't touch your repository.

That's intentional.

The next major step

Once this works, we'll move to Stage 5B:

              Pipeline FAILED
                     ↓
                Analyze Log
                     ↓
                Root Cause
                     ↓
               Generate Fix
                     ↓
             ┌───────────────┐
             │ HUMAN APPROVAL│
             └───────┬───────┘
                     ↓
              Create Git Branch
                     ↓
              Modify Repository
                     ↓
                  Commit
                     ↓
               Create PR
                     ↓
                Run CI

And we'll start with the pandas failure, because it's relatively safe: the agent can modify the workflow to install pandas.

Run python agent.py with the new prompt and send me the output. Then we'll build the GitHub branch/PR part.

##################OUTPUT######################
======================================================================

Sending log to Gemini AI...
Gemini attempt 1/3...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.


======================================================================
AI TROUBLESHOOTING REPORT
======================================================================
Failure Category : Missing Dependency
Root Cause       : The Python environment does not have the 'pandas' package installed when executing src/app.py.
Failed File      : src/app.py
Failed Line      : 22
Error Message    : ModuleNotFoundError: No module named 'pandas'
Explanation      : Execution of src/app.py failed at line 22 during 'import pandas' because the 'pandas' dependency has not been installed in the workflow's Python environment.
Recommended Fix  : Install 'pandas' prior to running the script (e.g., via 'pip install pandas' or by installing dependencies from requirements.txt).
Confidence       : 100%
Fix Type         : dependency

Proposed Changes:

File   : src/app.py
Change : Ensure pandas is installed in the CI environment or remove the import if unused.
======================================================================

############################################################################

Perfect. ✅ Stage 5A is working.

Your agent is now producing both:

Diagnosis
Fix type
Proposed change

For example:

Failure: Missing Dependency
Root Cause: pandas is not installed
Fix Type: dependency

Proposed Change:
src/app.py
→ Ensure pandas is installed
One thing I would improve before Stage 5B

Gemini proposed:

src/app.py — Ensure pandas is installed in the CI environment or remove the import if unused.

That's slightly ambiguous. The agent should ideally identify the actual file that needs changing. In this case, the correct remediation is probably the CI dependency configuration, not src/app.py.

So let's make the AI more precise.

Change this rule in your prompt:

- Each proposed change must contain:
    - file: repository-relative file path
    - change: specific modification to make

to:

- Each proposed change must contain:
    - file: repository-relative file path
    - change: exact change required

- Prefer modifying the file that caused the configuration,
  dependency, or workflow problem rather than the application
  source file.

- For missing Python dependencies, prefer requirements.txt
  or the CI workflow configuration if those files are present.

- Do not suggest removing an import merely to make CI pass
  unless the log clearly indicates the import is unused.

This should produce something more like:

Fix Type: dependency

Proposed Changes:

File: requirements.txt

Change: Add pandas to the dependency list.

or:

File: .github/workflows/ci.yml

Change: Change pip install pytest to pip install pytest pandas.

#########################OUTPUT################################
======================================================================

Sending log to Gemini AI...
Gemini attempt 1/3...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.


======================================================================
AI TROUBLESHOOTING REPORT
======================================================================
Failure Category : Dependency Failure
Root Cause       : The required Python dependency 'pandas' is not installed in the CI environment.
Failed File      : src/app.py
Failed Line      : 22
Error Message    : ModuleNotFoundError: No module named 'pandas'
Explanation      : Execution of src/app.py failed at line 22 because the Python module 'pandas' is not installed in the CI runner environment.
Recommended Fix  : Add 'pandas' to requirements.txt or install it in the CI workflow before running the application.
Confidence       : 100%
Fix Type         : dependency

Proposed Changes:

File   : requirements.txt
Change : Add 'pandas' to requirements.txt
======================================================================

###########################################################

Stage 5B — Human-approved GitHub fix

Now we're ready for the exciting part.

We'll have your agent create a fix branch and Pull Request, but only after you explicitly approve the proposed fix.

The flow will become:

                 GitHub Actions
                       ↓
                    FAILURE
                       ↓
                  AI Agent
                       ↓
                 Analyze Log
                       ↓
                Generate Fix
                       ↓
              ┌────────────────┐
              │ Proposed Fix   │
              └───────┬────────┘
                      ↓
                USER APPROVAL
                      ↓
              ┌───────┴────────┐
              │                │
             YES               NO
              ↓                ↓
        Create branch         Stop
              ↓
        Apply modification
              ↓
            Commit
              ↓
          Create PR
              ↓
        GitHub Actions

This is a much better POC than allowing the AI to directly modify main.

We'll start very safely

For the first implementation, the agent will NOT automatically merge anything.

It will only:

Create a branch
Make the proposed change
Commit it
Create a Pull Request

You review the PR and GitHub Actions tests it.

If the pipeline passes → great.

If it fails → that's actually even more interesting, because we can make the agent analyze the new failure and iterate.

That's the beginning of the true agentic loop.

Your current Stage 5A is complete. The next code we add will be the GitHub branch/commit/PR capability.



Great. Let's move to Stage 5B — create a GitHub branch + Pull Request, but we'll keep it safe: no automatic merge.

Before we write the code, I want to make one small architectural change: the agent should first show the proposed fix and ask for approval. Once approved, it can create the branch/PR.

We'll implement that in the next step.


Perfect. Let's build Stage 5B.1 — human approval + GitHub branch creation.

We will not modify any files yet. First we'll prove that the agent can safely create a branch.

1. Add this function to agent.py

Put it above main():

def create_fix_branch(repo, failed_run_id):

    branch_name = f"ai-fix/{failed_run_id}"

    print("\n")
    print("=" * 70)
    print("PROPOSED FIX BRANCH")
    print("=" * 70)

    print(f"Branch: {branch_name}")

    approval = input("\nCreate this branch? (yes/no): ").strip().lower()

    if approval != "yes":
        print("Operation cancelled.")
        return None

    # Get current default branch
    default_branch = repo.default_branch

    print(f"Base branch: {default_branch}")

    # Get latest commit on default branch
    base_branch = repo.get_branch(default_branch)
    base_sha = base_branch.commit.sha

    # Create branch reference
    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=base_sha
    )

    print(f"\nBranch created successfully: {branch_name}")

    return branch_name
2. Call the function after the AI report

Find this part near the end:

print(f"Confidence       : {analysis['confidence']}%")

After the proposed changes loop, add:

# --------------------------------------------------
# Human approval
# --------------------------------------------------

print("\n")
print("=" * 70)
print("HUMAN APPROVAL REQUIRED")
print("=" * 70)

print("The agent has NOT modified your repository.")

branch_name = create_fix_branch(
    repo,
    failed_run.id
)

if branch_name:
    print("\nReady for the next step:")
    print("Apply the AI-generated fix to this branch.")
3. Run it
python agent.py

You should now get:

AI TROUBLESHOOTING REPORT
======================================================================

Failure Category : Missing Dependency
Root Cause       : pandas is not installed
...

Proposed Changes:

File   : requirements.txt
Change : Add pandas to the dependency list.

======================================================================
HUMAN APPROVAL REQUIRED
======================================================================

The agent has NOT modified your repository.

======================================================================
PROPOSED FIX BRANCH
======================================================================

Branch: ai-fix/33642078288

Create this branch? (yes/no):

Type:

yes

You should then see:

Base branch: main

Branch created successfully: ai-fix/33642078288
4. Verify on GitHub

Open your repository's Branches page and you should see:

main
ai-fix/33642078288

At this point our agent has successfully done:

GitHub failure
      ↓
AI diagnosis
      ↓
AI proposed fix
      ↓
👤 Human approval
      ↓
Create isolated branch

It has still made zero changes to main. 👍

Next step

Once you confirm the branch appears on GitHub, we'll implement:

Stage 5B.2 — AI-generated code change → commit to the new branch

For your current pandas failure, the agent will be able to make a change such as:

requirements.txt

+ pandas

and commit it to:

ai-fix/33642078288

Then we'll add the final piece:

Branch
  ↓
Commit
  ↓
Pull Request
  ↓
GitHub Actions
  ↓
PASS / FAIL

Run it and tell me whether ai-fix/33642078288 appears in GitHub.

#######################OUTPUT#####################
======================================================================
HUMAN APPROVAL REQUIRED
======================================================================
The agent has NOT modified your repository.


======================================================================
PROPOSED FIX BRANCH
======================================================================
Branch: ai-fix/33724849012

Create this branch? (yes/no): yes
Base branch: main

Branch created successfully: ai-fix/33724849012

Ready for the next step:
Apply the AI-generated fix to this branch.
Fix Type         : dependency

Proposed Changes:

File   : requirements.txt
Change : Add 'pandas' to requirements.txt
======================================================================
###################################################################

Excellent. ✅ Stage 5B.1 is complete.

Your agent successfully:

Failed Pipeline
      ↓
Gemini Diagnosis
      ↓
Proposed Fix
      ↓
Human Approval: YES
      ↓
Created Branch
ai-fix/33724849012

And importantly, main is untouched.

Stage 5B.2 — Apply the AI-generated fix

Now we'll make the agent actually modify the new branch.

For this test, the fix is simple:

requirements.txt
+ pandas
1. Add this function to agent.py

Put it above main():

def apply_fix(repo, branch_name, analysis):

    print("\n")
    print("=" * 70)
    print("APPLYING AI-GENERATED FIX")
    print("=" * 70)

    changes = analysis.get("proposed_changes", [])

    if not changes:
        print("No proposed changes found.")
        return False

    for change in changes:

        file_path = change["file"]
        description = change["change"]

        print(f"\nFile: {file_path}")
        print(f"Change: {description}")

        # --------------------------------------------------
        # Special handling for requirements.txt
        # --------------------------------------------------

        if file_path == "requirements.txt":

            try:
                file = repo.get_contents(
                    file_path,
                    ref=branch_name
                )

                current_content = file.decoded_content.decode("utf-8")

                if "pandas" in current_content.lower():

                    print("pandas is already present.")
                    continue

                new_content = current_content.rstrip() + "\npandas\n"

                repo.update_file(
                    path=file_path,
                    message="AI fix: add missing pandas dependency",
                    content=new_content,
                    sha=file.sha,
                    branch=branch_name
                )

                print("Successfully updated requirements.txt")

            except Exception as e:

                print(f"Failed to update {file_path}: {e}")
                return False

        else:

            print(
                f"Automatic modification for {file_path} "
                f"is not implemented yet."
            )

            return False

    return True
2. Call it after the branch is created

Find:

if branch_name:
    print("\nReady for the next step:")
    print("Apply the AI-generated fix to this branch.")

Replace it with:

if branch_name:

    print("\nReady to apply the AI-generated fix.")

    approval = input(
        "\nApply the proposed fix to this branch? (yes/no): "
    ).strip().lower()

    if approval == "yes":

        success = apply_fix(
            repo,
            branch_name,
            analysis
        )

        if success:

            print("\n")
            print("=" * 70)
            print("AI FIX APPLIED SUCCESSFULLY")
            print("=" * 70)

            print(f"Branch: {branch_name}")

        else:

            print("\nFix could not be applied.")

    else:

        print("\nFix application cancelled.")
3. Run the agent
python agent.py

You'll go through:

HUMAN APPROVAL REQUIRED

Branch: ai-fix/33724849012

Create this branch? (yes/no): yes

Then:

Ready to apply the AI-generated fix.

Apply the proposed fix to this branch? (yes/no):

Enter:

yes

You should see:

======================================================================
APPLYING AI-GENERATED FIX
======================================================================

File: requirements.txt
Change: Add 'pandas' to requirements.txt

Successfully updated requirements.txt

======================================================================
AI FIX APPLIED SUCCESSFULLY
======================================================================

Branch: ai-fix/33724849012
4. Verify before we do anything else

Go to GitHub and open:

ai-fix/33724849012

Open requirements.txt.

You should see:

pytest
pandas

The change should exist only on the AI branch.

Your main branch should still be unchanged.

⚠️ Important

We're deliberately not creating the Pull Request yet.

Our progression is:

                 AI CI/CD Agent
                       │
                       ▼
                 Detect Failure ✅
                       │
                       ▼
                 Extract Log ✅
                       │
                       ▼
                 AI Diagnosis ✅
                       │
                       ▼
                 Generate Fix ✅
                       │
                       ▼
                Human Approval ✅
                       │
                       ▼
                Create Branch ✅
                       │
                       ▼
              Apply Fix to Branch ← YOU ARE HERE
                       │
                       ▼
                 Create PR
                       │
                       ▼
                 CI Re-runs
                       │
                  ┌────┴────┐
                  ▼         ▼
                 PASS      FAIL

Once you confirm requirements.txt contains pandas on the new branch, we'll implement Stage 5B.3 — automatically create the Pull Request.
