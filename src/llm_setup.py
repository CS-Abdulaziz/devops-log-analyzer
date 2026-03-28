import os
import json
from groq import Groq
from dotenv import load_dotenv
from agent.prompts import SYSTEM_PROMPT


# 1. Load environment variables from the .env file
load_dotenv()


class LogAnalyzer:

    """
    Expert DevOps Log Analyzer using Llama-3 (Groq API).
    Categorizes logs into: Docker, Kubernetes, System, Database, Memory, Network.
    """

    def __init__(self):

        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Please check your .env file.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"

    def analyze_log(self, log_entry, system_prompt):

        """
        Analyzes a log entry and returns a structured JSON diagnosis.
        """
        # --- Few-Shot Examples (Boosting Accuracy) ---

        messages = [

            {"role": "system", "content": system_prompt},
            
            # Example 1: Database Issue
            {"role": "user", "content": "ERROR: Connection refused to database at 172.18.0.3:5432"},
            {"role": "assistant", "content": json.dumps({
                "issue_type": "Database connectivity failure",
                "root_cause": "Database server is unreachable or port 5432 is blocked.",
                "suggested_fixes": [
                    "Check the database service status",
                    "Verify port 5432 is reachable from the application host",
                    "Validate database credentials and connection settings",
                ],
                "confidence": 0.95
            })},

            # Example 2: Memory Issue
            {"role": "user", "content": "java.lang.OutOfMemoryError: Java heap space"},
            {"role": "assistant", "content": json.dumps({
                "issue_type": "JVM memory exhaustion",
                "root_cause": "Application exhausted JVM heap memory.",
                "suggested_fixes": [
                    "Increase the JVM heap limit with -Xmx",
                    "Inspect the application for memory leaks",
                    "Review recent traffic or workload spikes",
                ],
                "confidence": 0.98
            })},

            # Example 3: Kubernetes Issue
            {"role": "user", "content": "Back-off restarting failed container in pod-xyz"},
            {"role": "assistant", "content": json.dumps({
                "issue_type": "Kubernetes container restart loop",
                "root_cause": "Pod in CrashLoopBackOff state due to runtime failure.",
                "suggested_fixes": [
                    "Inspect the failing container logs with kubectl logs pod-xyz",
                    "Describe the pod to review recent events",
                    "Validate the container command, environment, and mounted secrets",
                ],
                "confidence": 0.92
            })},

            # Actual Log Entry from User
            {"role": "user", "content": log_entry}
        ]

        try:
            # Making the call to Groq
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Keep it static and deterministic
                response_format={"type": "json_object"}
            )
            
            # Parse and return the JSON response
            return json.loads(completion.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"LLM Analysis failed: {str(e)}"}


# Just testing the results of the model
analyzer = LogAnalyzer()
sample_log = """
        Exception in thread "main" java.lang.NullPointerException
        at com.example.service.UserService.getUser(UserService.java:45)
        at com.example.controller.UserController.get(UserController.java:22)
    """

print("--- AI Analysis Result ---")
result = analyzer.analyze_log(sample_log, SYSTEM_PROMPT)
print(json.dumps(result, indent=4))
