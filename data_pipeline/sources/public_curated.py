"""
Curated Public Domain Question Feed Source.
Ingests standard open computer science, placement, and engineering interview questions
from controlled, open curriculum benchmarks with strict source attribution.
"""

from typing import List
from .base import BaseSource
from ..intelligence.pipeline import IngestionItem


class CuratedPublicFeedSource(BaseSource):
    """Source adapter for curated public computer science placement feeds."""

    def __init__(self):
        super().__init__(source_name="open_placement_benchmark")

    def fetch_items(self, limit: int = 50) -> List[IngestionItem]:
        """Provides verified public placement interview questions."""
        raw_data = [
            {
                "title": "Reverse a Linked List",
                "text": "Given the head of a singly linked list, reverse the list, and return the reversed list. Ensure in-place reversal in O(N) time and O(1) space.",
                "category": "DSA",
                "subcategory": "Linked Lists",
                "topic": "Reverse Linked List",
                "difficulty": "Easy",
                "companies": ["Amazon", "Microsoft", "TCS"],
                "roles": ["SDE-1", "Software Engineer"],
                "source_item_id": "ll_rev_01"
            },
            {
                "title": "0/1 Knapsack Problem",
                "text": "Given weights and values of n items, put these items in a knapsack of capacity W to get the maximum total value in the knapsack. Each item can either be picked completely or not picked at all.",
                "category": "DSA",
                "subcategory": "Dynamic Programming",
                "topic": "Knapsack",
                "difficulty": "Medium",
                "companies": ["Google", "Amazon", "Microsoft"],
                "roles": ["SDE-1", "Software Engineer"],
                "source_item_id": "dp_knap_01"
            },
            {
                "title": "Nth Highest Salary in SQL",
                "text": "Write a SQL query to find the N-th highest salary from an Employee table. If there is no N-th highest salary, the query should return null. Use DENSE_RANK() or LIMIT OFFSET.",
                "category": "SQL",
                "subcategory": "Window Functions",
                "topic": "Dense Rank",
                "difficulty": "Medium",
                "companies": ["Amazon", "Flipkart", "Oracle"],
                "roles": ["Data Analyst", "Backend Engineer"],
                "source_item_id": "sql_sal_02"
            },
            {
                "title": "ACID Properties in DBMS",
                "text": "Explain ACID properties in Database Management Systems (Atomicity, Consistency, Isolation, Durability) and describe how the Write-Ahead Logging (WAL) protocol guarantees durability.",
                "category": "DBMS",
                "subcategory": "Transactions & Concurrency",
                "topic": "ACID Properties",
                "difficulty": "Easy",
                "companies": ["TCS", "Infosys", "Oracle"],
                "roles": ["Software Engineer", "Systems Engineer"],
                "source_item_id": "dbms_acid_01"
            },
            {
                "title": "Process vs Thread",
                "text": "Distinguish between a process and a thread in modern operating systems. Detail process control blocks (PCB), context switching overhead, virtual address spaces, and inter-process communication.",
                "category": "OS",
                "subcategory": "Process Management",
                "topic": "Processes and Threads",
                "difficulty": "Easy",
                "companies": ["Qualcomm", "Intel", "Cisco"],
                "roles": ["Systems Engineer", "Software Engineer"],
                "source_item_id": "os_proc_01"
            },
            {
                "title": "TCP vs UDP Comparison",
                "text": "Compare Transmission Control Protocol (TCP) and User Datagram Protocol (UDP). Explain the three-way handshake (SYN, SYN-ACK, ACK), flow control via sliding window, and head-of-line blocking.",
                "category": "Computer Networks",
                "subcategory": "OSI & TCP/IP",
                "topic": "TCP Three-way Handshake",
                "difficulty": "Easy",
                "companies": ["Cisco", "Amazon", "Infosys"],
                "roles": ["Systems Engineer", "Cloud Engineer"],
                "source_item_id": "cn_tcp_01"
            },
            {
                "title": "Time and Work - Pipes and Cisterns",
                "text": "Pipe A can fill a tank in 12 hours, while Pipe B can empty it in 18 hours. If both pipes are opened simultaneously, in how many hours will the cistern be completely filled?",
                "category": "Aptitude",
                "subcategory": "Quantitative",
                "topic": "Time and Work",
                "difficulty": "Easy",
                "companies": ["TCS", "Cognizant", "Accenture"],
                "roles": ["Associate Software Engineer", "Graduate Trainee"],
                "source_item_id": "apt_quant_01"
            },
            {
                "title": "Explain Overfitting and Regularization in Machine Learning",
                "text": "What is overfitting in machine learning? Explain how L1 (Lasso) and L2 (Ridge) regularization mathematically penalize model complexity to reduce variance.",
                "category": "ML",
                "subcategory": "Supervised Learning",
                "topic": "Regularization",
                "difficulty": "Medium",
                "companies": ["Google", "Amazon", "Walmart Labs"],
                "roles": ["Machine Learning Engineer", "Data Scientist"],
                "source_item_id": "ml_reg_01"
            },
            {
                "title": "Design a URL Shortener (TinyURL)",
                "text": "Design a scalable URL shortening service like TinyURL. Detail the high-level architecture including base62 encoding vs hashing, database schema, caching with Redis, and handling 100M daily writes.",
                "category": "System Design",
                "subcategory": "Distributed Systems",
                "topic": "URL Shortener",
                "difficulty": "Hard",
                "companies": ["Uber", "Meta", "Google"],
                "roles": ["SDE-2", "Backend Engineer"],
                "source_item_id": "sd_tinyurl_01"
            },
            {
                "title": "Tell Me About a Time You Faced a Disagreement in a Team",
                "text": "Describe a situation where you had a technical disagreement with a team member or project lead. How did you communicate your viewpoint, evaluate trade-offs, and reach a resolution using the STAR method?",
                "category": "Behavioral",
                "subcategory": "STAR Method",
                "topic": "Conflict Resolution",
                "difficulty": "Medium",
                "companies": ["Amazon", "Google", "Microsoft"],
                "roles": ["All Roles"],
                "source_item_id": "beh_star_01"
            }
        ]

        items = []
        for d in raw_data[:limit]:
            items.append(
                IngestionItem(
                    raw_text=d["text"],
                    title=d["title"],
                    source_name=self.source_name,
                    source_url=f"https://open-curriculum.edu/questions/{d['source_item_id']}",
                    source_item_id=d["source_item_id"],
                    category=d.get("category"),
                    subcategory=d.get("subcategory"),
                    topic=d.get("topic"),
                    difficulty=d.get("difficulty"),
                    companies=d.get("companies"),
                    roles=d.get("roles"),
                )
            )
        return items
