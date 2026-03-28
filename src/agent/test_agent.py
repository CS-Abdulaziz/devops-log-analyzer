from agent.agent import analyze_log
from agent.judge import judge_response



log = """
ERROR: Connection refused to database at 172.18.0.3:5432
"""

result = analyze_log(log)
print(result)

judge = judge_response(log, result.model_dump())
print(judge)