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



🎉 Excellent! This is a major milestone.

Your AI CI/CD agent has now successfully completed the automated fix application:

GitHub Actions failure
        ↓
Agent detects failed job
        ↓
Downloads logs
        ↓
Extracts failure
        ↓
Gemini diagnoses
        ↓
Classifies as dependency issue
        ↓
Human approves fix
        ↓
Creates fix branch
        ↓
Modifies CI workflow
        ↓
Commits change
        ↓
✅ SUCCESS

Your commit is:

f4d099a188b4c0caf71afa851f109b0dd77cf3c0

and branch:

ai-fix/33724849012
Next step: Create the Pull Request

Now we want the agent to automatically do:

AI Fix Branch
      ↓
Create Pull Request
      ↓
GitHub Actions runs
      ↓
Pipeline passes/fails
      ↓
Agent reports result

This is important because we don't want the agent directly merging its own fix. The PR gives you the human-review gate.

Don't change anything yet

Your current implementation has successfully reached the point we wanted.

Next we'll add a small create_pull_request() function to agent.py and call it after apply_fix() succeeds.

That will give your POC a very compelling end-to-end story:

"An AI agent autonomously investigates a failed GitHub Actions pipeline, identifies the root cause, proposes a fix, obtains human approval, creates a fix branch, applies the change, and raises a Pull Request for validation."

That's already a solid AI-powered CI/CD troubleshooting agent POC.


Great. We are at the PR stage now. Your current main() already calls apply_fix() and checks its success result.

We will make one small addition: after the fix is successfully committed, create a Pull Request.

Step 1 — Add this function

In agent.py, add this function just before main():

def create_pull_request(repo, branch_name, analysis):

    print("\n")
    print("=" * 70)
    print("CREATING PULL REQUEST")
    print("=" * 70)

    base_branch = repo.default_branch

    title = (
        f"AI Fix: {analysis['failure_category']}"
    )

    body = f"""
## AI-Generated CI/CD Fix

### Failure

**Category:** {analysis['failure_category']}

**Root Cause:**
{analysis['root_cause']}

**Error:**
{analysis['error_message']}

### AI Recommended Fix

{analysis['recommended_fix']}

### Proposed Changes

"""

    for change in analysis["proposed_changes"]:

        body += (
            f"- `{change['file']}`: "
            f"{change['change']}\n"
        )

    body += """
### Validation

This Pull Request was created by the AI CI/CD troubleshooting agent.

The GitHub Actions pipeline should validate the proposed fix.
"""

    try:

        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base=base_branch
        )

        print("\n")
        print("=" * 70)
        print("PULL REQUEST CREATED")
        print("=" * 70)

        print(f"PR Number : #{pr.number}")
        print(f"Title     : {pr.title}")
        print(f"URL       : {pr.html_url}")

        return pr

    except Exception as e:

        print("\nFailed to create Pull Request:")
        print(e)

        return None
Step 2 — Modify the successful apply_fix() section

You currently have something like:

if success:

    print("\n")
    print("=" * 70)
    print("AI FIX APPLIED SUCCESSFULLY")
    print("=" * 70)

    print(f"Branch: {branch_name}")

This is in the main() flow after apply_fix() succeeds.

Change it to:

if success:

    print("\n")
    print("=" * 70)
    print("AI FIX APPLIED SUCCESSFULLY")
    print("=" * 70)

    print(f"Branch: {branch_name}")

    # --------------------------------------------------
    # Create Pull Request
    # --------------------------------------------------

    pr = create_pull_request(
        repo,
        branch_name,
        analysis
    )

    if pr:

        print("\nPull Request is ready for review.")

    else:

        print("\nPull Request could not be created.")

That's it. Only two changes.

Step 3 — Run the agent
python agent.py

Because your branch already exists:

Branch already exists: ai-fix/33724849012
Using the existing branch.

Then approve:

Apply the proposed fix to this branch? (yes/no): yes

You should get:

AI FIX APPLIED SUCCESSFULLY

File   : .github/workflows/ci.yml
Branch : ai-fix/33724849012
Commit : f4d099...

Then:

======================================================================
CREATING PULL REQUEST
======================================================================

PULL REQUEST CREATED
======================================================================

PR Number : #1
Title     : AI Fix: Missing Dependency
URL       : https://github.com/...
⚠️ One thing before you run

You already have the branch and commit:

ai-fix/33724849012
        ↓
f4d099a188b4c0caf71afa851f109b0dd77cf3c0

So if you run the whole agent again, it may try to apply the same fix again.

That's okay for now, but if GitHub says the branch is already up to date / no changes, send me that output.

Our POC is becoming:
             GitHub Actions
                   │
                   ▼
             Pipeline fails
                   │
                   ▼
          ┌─────────────────┐
          │   AI Agent      │
          │                 │
          │ Get failure     │
          │ Get logs        │
          │ Extract error   │
          │ Gemini analysis │
          └────────┬────────┘
                   │
                   ▼
            Human approval
                   │
                   ▼
              Fix branch
                   │
                   ▼
             Apply AI fix
                   │
                   ▼
             Create PR
                   │
                   ▼
          GitHub Actions CI
                   │
             ┌─────┴─────┐
             ▼           ▼
           PASS         FAIL

Run it and send me the output from CREATING PULL REQUEST onward. Then we'll implement the next important piece: the agent waits for the PR's GitHub Actions result and tells you whether the AI fix actually worked.

####################OUTPUT#################################

Target file  : .github/workflows/ci.yml
Target branch: ai-fix/33724849012

Current dependency installation:
----------------------------------------------------------------------
          python -m pip install --upgrade pip
          pip install pytest pandas

pandas is already installed.


======================================================================
AI FIX APPLIED SUCCESSFULLY
======================================================================
Branch: ai-fix/33724849012


======================================================================
CREATING PULL REQUEST
======================================================================


======================================================================
PULL REQUEST CREATED
======================================================================
PR Number : #1
Title     : AI Fix: Dependency Failure
URL       : https://github.com/sahnawaj/ai-cicd-troubleshooter/pull/1

Pull Request is ready for review.
Fix Type         : dependency

Proposed Changes:

File   : requirements.txt
Change : pandas
======================================================================
###########################################################

🎉 Excellent! Your POC has now successfully reached the Pull Request stage.

You have:

Pipeline failure
      ↓
AI analyzes logs
      ↓
AI identifies missing pandas
      ↓
Human approves
      ↓
AI creates branch
      ↓
AI applies fix
      ↓
AI creates PR #1
      ↓
       ⭐ NEXT
GitHub Actions validates the fix

Your PR is:

#1 — AI Fix: Dependency Failure

Now let's make the agent automatically wait for GitHub Actions and report whether the fix passed or failed.


Stage 5C — Monitor the Pull Request

We will add one function.

Step 1 — Add this function to agent.py

Put it just before main(), underneath create_pull_request():

def monitor_pull_request(repo, pr, timeout=300):

    print("\n")
    print("=" * 70)
    print("MONITORING PULL REQUEST")
    print("=" * 70)

    print(f"PR Number : #{pr.number}")
    print(f"URL       : {pr.html_url}")

    start_time = time.time()

    while True:

        # Refresh PR information
        pr.update()

        head_sha = pr.head.sha

        print(f"\nCommit: {head_sha}")

        try:

            commit = repo.get_commit(head_sha)

            check_runs = list(
                commit.get_check_runs()
            )

        except Exception as e:

            print(f"Unable to get CI status: {e}")

            return False

        if not check_runs:

            print("GitHub Actions has not started yet.")

        else:

            all_completed = True

            for check in check_runs:

                print(
                    f"Check: {check.name} | "
                    f"Status: {check.status} | "
                    f"Conclusion: {check.conclusion}"
                )

                if check.status != "completed":

                    all_completed = False

            # --------------------------------------------------
            # Wait until all checks finish
            # --------------------------------------------------

            if all_completed:

                failed = False

                for check in check_runs:

                    if check.conclusion not in [
                        "success",
                        "skipped",
                        "neutral"
                    ]:

                        failed = True

                print("\n")
                print("=" * 70)

                if failed:

                    print("AI FIX VALIDATION FAILED")
                    print("=" * 70)

                    print(
                        "\nThe Pull Request CI checks failed."
                    )

                    print(
                        "The AI-generated fix needs further investigation."
                    )

                    return False

                else:

                    print("AI FIX VALIDATED SUCCESSFULLY")
                    print("=" * 70)

                    print(
                        "\nAll GitHub Actions checks passed."
                    )

                    print(
                        "The proposed AI fix appears to be working."
                    )

                    return True

        # --------------------------------------------------
        # Timeout
        # --------------------------------------------------

        if time.time() - start_time > timeout:

            print("\n")
            print("=" * 70)
            print("CI MONITORING TIMEOUT")
            print("=" * 70)

            print(
                "\nGitHub Actions did not finish within "
                f"{timeout} seconds."
            )

            return False

        print("\nWaiting 10 seconds for CI...")

        time.sleep(10)
Step 2 — Call it after PR creation

You currently have:

if pr:

    print("\nPull Request is ready for review.")

else:

    print("\nPull Request could not be created.")

Change it to:

if pr:

    print("\nPull Request is ready for review.")

    # --------------------------------------------------
    # Monitor GitHub Actions
    # --------------------------------------------------

    ci_success = monitor_pull_request(
        repo,
        pr
    )

    if ci_success:

        print("\n")
        print("=" * 70)
        print("END-TO-END AI FIX SUCCESS")
        print("=" * 70)

    else:

        print("\n")
        print("=" * 70)
        print("AI FIX REQUIRES FURTHER INVESTIGATION")
        print("=" * 70)

else:

    print("\nPull Request could not be created.")
Step 3 — Run the agent

Now:

python agent.py
One thing to expect

Because your existing branch already contains:

pip install pytest pandas

the agent may say:

pandas is already installed.

That's okay.

It will then create/use the PR and reach:

MONITORING PULL REQUEST

You should see something like:

======================================================================
MONITORING PULL REQUEST
======================================================================

PR Number : #1
URL       : https://github.com/.../pull/1

Commit: f4d099a...

Check: CI Pipeline | Status: queued | Conclusion: None

Waiting 10 seconds for CI...

Then:

Check: CI Pipeline | Status: in_progress | Conclusion: None

Waiting 10 seconds for CI...

Finally:

Check: CI Pipeline | Status: completed | Conclusion: success

and:

======================================================================
AI FIX VALIDATED SUCCESSFULLY
======================================================================

All GitHub Actions checks passed.
The proposed AI fix appears to be working.
🎯 This is now a real agentic workflow

After this step, your demo becomes quite strong:

             GitHub
                │
                ▼
        Pipeline fails ❌
                │
                ▼
       ┌─────────────────┐
       │   AI Agent      │
       │                 │
       │ Fetch logs      │
       │ Extract error   │
       │ Diagnose        │
       │ Classify        │
       │ Propose fix     │
       └────────┬────────┘
                │
                ▼
        Human Approval
                │
                ▼
          Create Branch
                │
                ▼
           Apply Fix
                │
                ▼
         Create Pull Request
                │
                ▼
       GitHub Actions runs
                │
          ┌─────┴─────┐
          ▼           ▼
        PASS         FAIL
          │           │
          ▼           ▼
       SUCCESS     Investigate

And importantly, the agent doesn't merge the code itself. The human still controls the final merge.

After this works

The next improvement I'd recommend is not more code yet. We should make the agent handle the interesting case:

What happens when the AI's first fix fails?

Then we can implement:

PR CI fails
   ↓
Agent gets NEW failure logs
   ↓
Gemini analyzes new failure
   ↓
Proposes Fix #2
   ↓
Human approval
   ↓
Update same PR
   ↓
CI runs again

That is where this starts becoming a genuinely agentic CI/CD troubleshooting system, rather than just a log analyzer.

####################OUTPUT#############################
CREATING PULL REQUEST
======================================================================

Pull Request already exists.
PR Number : #1
URL       : https://github.com/sahnawaj/ai-cicd-troubleshooter/pull/1

Pull Request is ready for review.


======================================================================
MONITORING PULL REQUEST
======================================================================
PR Number : #1
URL       : https://github.com/sahnawaj/ai-cicd-troubleshooter/pull/1

Commit: f4d099a188b4c0caf71afa851f109b0dd77cf3c0
Check: build-and-test | Status: completed | Conclusion: success


======================================================================
AI FIX VALIDATED SUCCESSFULLY
======================================================================

All GitHub Actions checks passed.
The proposed AI fix appears to be working.


======================================================================
END-TO-END AI FIX SUCCESS
======================================================================
Fix Type         : dependency

Proposed Changes:

File   : requirements.txt
Change : Add pandas to requirements.txt
======================================================================
############################################################
🎉 This is exactly what we wanted. Your end-to-end POC is working.

You now have a complete autonomous troubleshooting loop:

GitHub Actions Pipeline
        │
        ▼
    ❌ Failure
        │
        ▼
   AI CI/CD Agent
        │
        ├── Find failed workflow
        ├── Find failed job
        ├── Download logs
        ├── Extract relevant error
        ├── Send to Gemini
        └── Diagnose failure
        │
        ▼
   AI Proposed Fix
        │
        ▼
  👤 Human Approval
        │
        ▼
  Create Fix Branch
        │
        ▼
   Apply AI Fix
        │
        ▼
 Create / Reuse Pull Request
        │
        ▼
 GitHub Actions runs
        │
        ▼
    ✅ SUCCESS

Your actual run proves it:

PR #1
    ↓
build-and-test
    ↓
completed / success
    ↓
AI FIX VALIDATED SUCCESSFULLY
What I recommend as the next stage

Don't add more complexity immediately. We should now make the POC more impressive by adding the missing failure → retry → second fix capability.

For example:

Pipeline fails
     ↓
Gemini: "pandas missing"
     ↓
AI fixes pandas
     ↓
PR created
     ↓
CI fails again
     ↓
Agent detects NEW failure
     ↓
Gemini analyzes NEW logs
     ↓
AI proposes Fix #2
     ↓
Human approval
     ↓
Apply Fix #2
     ↓
CI passes

That demonstrates genuine agentic behavior, rather than simply:

"Send logs to an LLM and get an answer."

Your current POC capabilities
Capability    Status
GitHub authentication    ✅
Detect failed workflow    ✅
Detect failed job    ✅
Download job logs    ✅
Extract relevant failure    ✅
Gemini analysis    ✅
Failure categorization    ✅
Root-cause identification    ✅
Proposed code/config fix    ✅
Human approval    ✅
Create fix branch    ✅
Apply fix    ✅
Create/reuse PR    ✅
Monitor PR CI    ✅
Validate fix automatically    ✅
Retry with a second fix    ⏭️ Next
Auto-merge    ❌ Intentionally not doing this

I would keep auto-merge disabled for this POC. Human approval + automated validation is a much better enterprise story.

One thing I'd also fix

Your final report still says:

File : requirements.txt
Change : Add pandas

while the actual change was:

.github/workflows/ci.yml
pip install pytest pandas

That's a reporting inconsistency we should fix before presenting this POC. The agent should report the actual file and actual change committed, not merely Gemini's original proposal.

So I suggest our next two steps:

1. Fix the reporting accuracy
2. Add automatic second-attempt troubleshooting when PR CI fails

That will make this considerably stronger for your AI-Powered CI/CD project/demo.

#####################OUTPUT######################
======================================================================
MONITORING PULL REQUEST
======================================================================
PR Number : #1
URL       : https://github.com/sahnawaj/ai-cicd-troubleshooter/pull/1

Commit: f4d099a188b4c0caf71afa851f109b0dd77cf3c0
Check: build-and-test | Status: completed | Conclusion: success


======================================================================
AI FIX VALIDATED SUCCESSFULLY
======================================================================

All GitHub Actions checks passed.
The proposed AI fix appears to be working.


======================================================================
END-TO-END AI FIX SUCCESS
======================================================================


======================================================================
FINAL AI FIX REPORT
======================================================================
Fix Type : dependency

ACTUAL CHANGE APPLIED:
File   : .github/workflows/ci.yml
Change : pandas already installed
======================================================================

#################################################


Great. We'll do Step 2 only: add the retry/feedback loop.

The goal is:

PR CI fails
   ↓
Agent gets the new failure
   ↓
Gemini analyzes it
   ↓
Proposes Fix #2
   ↓
Human approves
   ↓
Agent applies Fix #2
   ↓
CI runs again

Before changing the code, I want to use your current agent_fixed.py as the starting point so we don't accidentally overwrite the working parts.

Next, upload your current agent.py (the version you're running successfully now). Then I'll modify that exact file and give you a ready-to-run replacement, rather than asking you to manually merge a large block.
