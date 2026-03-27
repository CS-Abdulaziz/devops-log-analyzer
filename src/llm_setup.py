import os
import json
from groq import Groq
from dotenv import load_dotenv

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

    def analyze_log(self, log_entry):
        """
        Analyzes a log entry and returns a structured JSON diagnosis.
        """
        # --- The System Prompt (Logic & Constraints) ---
        system_instruction = (
            "You are an expert DevOps Incident Response Agent. Analyze logs "
            "and provide a structured diagnostic report.\n"
            "Constraints:\n"
            "1. Output MUST be a valid JSON object only.\n"
            "2. Categorize into EXACTLY: [Docker, Kubernetes, System, Database, Memory, Network].\n"
            "3. Severity levels: [Critical, High, Medium, Low].\n"
            "4. Suggest a 'fix' based on professional DevOps and StackOverflow knowledge."
        )

        # --- Few-Shot Examples (Boosting Accuracy) ---
        messages = [
            {"role": "system", "content": system_instruction},
            
            # Example 1: Database Issue
            {"role": "user", "content": "ERROR: Connection refused to database at 172.18.0.3:5432"},
            {"role": "assistant", "content": json.dumps({
                "category": "Database",
                "severity": "High",
                "root_cause": "Database server is unreachable or port 5432 is blocked.",
                "fix": "Check DB status, verify port 5432 is open, and validate credentials.",
                "confidence": 0.95
            })},

            # Example 2: Memory Issue
            {"role": "user", "content": "java.lang.OutOfMemoryError: Java heap space"},
            {"role": "assistant", "content": json.dumps({
                "category": "Memory",
                "severity": "Critical",
                "root_cause": "Application exhausted JVM heap memory.",
                "fix": "Increase memory limits (-Xmx) or check for memory leaks.",
                "confidence": 0.98
            })},

            # Example 3: Kubernetes Issue
            {"role": "user", "content": "Back-off restarting failed container in pod-xyz"},
            {"role": "assistant", "content": json.dumps({
                "category": "Kubernetes",
                "severity": "High",
                "root_cause": "Pod in CrashLoopBackOff state due to runtime failure.",
                "fix": "Use 'kubectl logs pod-xyz' to inspect container logs.",
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

# --- Local Verification Test ---
if __name__ == "__main__":
    analyzer = LogAnalyzer()
    
    # Example Test: System Disk Error
    sample_log = "kernel: [1234.56] sda1: write error: no space left on device"
    
    print("--- AI Analysis Result ---")
    result = analyzer.analyze_log(sample_log)
    print(json.dumps(result, indent=4))