READINESS_PROMPT_TEMPLATE = """
You are the Placement OS Readiness Intelligence Engine.
Analyze the following student performance data and return a JSON evaluation.

STUDENT TARGET:
- Target Role: {target_role}
- Target Company: {target_company}
- Preparation Weeks Remaining: {preparation_weeks}

PERFORMANCE & EVIDENCE SUMMARY:
- Assessment History: {assessment_history}
- Practice Performance: {practice_performance}
- Interview Performance: {interview_performance}
- Mistake Count & Patterns: {mistake_summary}
- Resume & Project Evidence: {evidence_summary}

Calculate dimension scores (0-100):
- aptitude
- dsa
- cs_fundamentals
- sql
- communication
- resume
- projects
- interview

Return ONLY a JSON object formatted as follows:
{{
    "overall_score": 72.0,
    "dimensions": {{
        "aptitude": 68.0,
        "dsa": 61.0,
        "cs_fundamentals": 74.0,
        "sql": 82.0,
        "communication": 70.0,
        "resume": 76.0,
        "projects": 73.0,
        "interview": 65.0
    }},
    "strengths": ["Strong SQL query optimization skills", "Good CS fundamentals in OS and DBMS"],
    "critical_gaps": ["Graph algorithms and DFS/BFS traversal", "Dynamic programming memoization"],
    "risk_areas": ["System design communication clarity under pressure"],
    "next_best_action": {{
        "action_id": "act_graph_dfs_bfs",
        "title": "Master BFS/DFS Graph Traversal",
        "type": "practice_topic",
        "description": "Solve 5 medium BFS/DFS problems to bridge graph traversal gap before shortest-path algorithms.",
        "target_dimension": "dsa",
        "estimated_minutes": 45,
        "priority": "high"
    }}
}}
"""
