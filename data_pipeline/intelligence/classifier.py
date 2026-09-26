"""
Question Taxonomy Classifier.
Classifies text and problem statements into one of the 26 canonical Placement OS taxonomies:
DSA, Programming, SQL, DBMS, OS, Computer Networks, OOP, Aptitude, AI, ML, DL, NLP,
Computer Vision, Generative AI, Cloud, DevOps, Data Analytics, Power BI, Excel,
Web Development, System Design, HR, Behavioral, Communication, Project, Resume.

Also extracts subcategory and topic keywords.
"""

import re
from typing import Dict, Any, Tuple, List
from ..config import SUPPORTED_TAXONOMIES


class TaxonomyClassifier:
    """Classifies questions into primary category, subcategory, and topic."""

    # Rich feature vocabularies with domain-weighted terms
    TAXONOMY_KEYWORDS: Dict[str, Dict[str, List[str]]] = {
        "DSA": {
            "Dynamic Programming": ["knapsack", "dp", "memoization", "longest common subsequence", "coin change", "edit distance", "optimal substructure", "fibonacci", "subset sum"],
            "Trees & Graphs": ["binary search tree", "bst", "inorder", "preorder", "postorder", "dfs", "bfs", "dijkstra", "topological sort", "graph", "tree", "lowest common ancestor"],
            "Arrays & Hashing": ["two sum", "prefix sum", "hashmap", "sliding window", "two pointer", "subarray", "kadane", "majority element", "anagram"],
            "Linked Lists": ["linked list", "reverse linked list", "floyd cycle", "detect cycle", "merge two sorted", "doubly linked"],
            "Greedy Algorithms": ["greedy", "fractional knapsack", "interval scheduling", "activity selection", "huffman coding"],
            "Binary Search": ["binary search", "search in rotated", "lower bound", "upper bound", "median of two sorted"]
        },
        "SQL": {
            "Queries & Joins": ["select", "inner join", "left join", "right join", "outer join", "cross join", "group by", "having", "where clause"],
            "Window Functions": ["row_number", "dense_rank", "rank()", "partition by", "lead", "lag", "ntile", "window function"],
            "Aggregations": ["count", "sum", "avg", "min", "max", "aggregate", "rollup", "cube"],
            "Subqueries & CTEs": ["with clause", "cte", "common table expression", "correlated subquery", "nested query"],
            "DML & DDL": ["create table", "alter table", "drop table", "truncate", "insert into", "update", "delete", "foreign key", "primary key"]
        },
        "DBMS": {
            "Transactions & Concurrency": ["acid", "atomicity", "consistency", "isolation", "durability", "deadlock", "2pl", "two phase locking", "dirty read", "phantom read"],
            "Normalization": ["normal form", "1nf", "2nf", "3nf", "bcnf", "functional dependency", "lossless join", "dependency preservation"],
            "Indexing & Architecture": ["b-tree", "b+ tree", "clustered index", "non-clustered index", "hashing", "query optimization", "wal", "write-ahead log"]
        },
        "OS": {
            "Process Management": ["process", "thread", "fork", "context switch", "pcb", "inter-process communication", "ipc", "shared memory", "message passing"],
            "CPU Scheduling": ["round robin", "sjf", "fcfs", "priority scheduling", "preemption", "scheduling algorithm", "turnaround time"],
            "Synchronization": ["deadlock", "mutual exclusion", "hold and wait", "circular wait", "no preemption", "bankers algorithm", "mutex", "semaphore", "critical section", "peterson solution", "race condition", "producer consumer", "dining philosophers", "readers writers"],
            "Memory Management": ["paging", "segmentation", "virtual memory", "page fault", "tlb", "lru", "page replacement", "belady anomaly", "thrashing"]
        },
        "Computer Networks": {
            "OSI & TCP/IP": ["osi model", "tcp/ip", "tcp vs udp", "three-way handshake", "syn ack", "flow control", "congestion control", "window size"],
            "Network Layer": ["ip address", "ipv4", "ipv6", "subnetting", "cidr", "routing", "ospf", "bgp", "arp", "icmp"],
            "Application Layer": ["http", "https", "dns", "dhcp", "ssl", "tls", "ftp", "smtp", "websocket"],
            "Security": ["firewall", "ddos", "man in the middle", "encryption", "public key", "vpn"]
        },
        "OOP": {
            "Core Pillars": ["polymorphism", "encapsulation", "inheritance", "abstraction", "method overloading", "method overriding", "virtual function", "interface", "abstract class"],
            "Design Principles": ["solid principles", "single responsibility", "open closed", "liskov substitution", "interface segregation", "dependency inversion"],
            "Design Patterns": ["singleton", "factory pattern", "observer pattern", "builder pattern", "strategy pattern", "decorator"]
        },
        "Programming": {
            "Python": ["python", "list comprehension", "generator", "decorator", "gil", "lambda", "yield", "dunder", "__init__"],
            "Java": ["java", "jvm", "garbage collection", "memory leak", "multithreading", "synchronized", "volatile", "hashcode", "equals"],
            "C++": ["c++", "pointers", "references", "smart pointers", "raii", "templates", "stl", "destructor", "vector"],
            "JavaScript": ["javascript", "closure", "promise", "async/await", "event loop", "prototype", "hoisting", "scope"]
        },
        "Aptitude": {
            "Quantitative": ["time and work", "speed time distance", "profit and loss", "simple interest", "compound interest", "percentages", "ratios", "permutation", "combination", "probability", "averages"],
            "Logical Reasoning": ["blood relations", "seating arrangement", "syllogisms", "direction sense", "coding decoding", "series completion", "data sufficiency"],
            "Verbal Ability": ["reading comprehension", "sentence correction", "synonyms", "antonyms", "idioms", "parajumbles", "grammar"]
        },
        "AI": {
            "Search & Planning": ["a* search", "minimax", "alpha beta pruning", "heuristic", "breadth first search", "state space", "agent"],
            "Knowledge Representation": ["expert system", "first order logic", "ontology", "inference engine", "rule based"]
        },
        "ML": {
            "Supervised Learning": ["linear regression", "logistic regression", "decision tree", "random forest", "svm", "support vector", "gradient boosting", "xgboost"],
            "Unsupervised Learning": ["k-means", "hierarchical clustering", "pca", "dimensionality reduction", "dbscan"],
            "Evaluation Metrics": ["roc auc", "precision", "recall", "f1-score", "confusion matrix", "cross validation", "bias variance tradeoff", "overfitting", "underfitting"]
        },
        "DL": {
            "Neural Networks": ["backpropagation", "gradient descent", "activation function", "relu", "sigmoid", "softmax", "loss function", "cross entropy", "dropout", "batch normalization"],
            "Architectures": ["cnn", "convolutional", "rnn", "lstm", "gru", "autoencoder", "vanishing gradient"]
        },
        "NLP": {
            "Text Processing": ["tokenization", "stemming", "lemmatization", "stop words", "tf-idf", "n-gram", "bag of words"],
            "Embeddings & Models": ["word2vec", "bert", "transformer", "attention mechanism", "pos tagging", "named entity recognition", "sentiment analysis"]
        },
        "Computer Vision": {
            "Image Processing": ["edge detection", "sobel", "canny", "kernel", "convolution", "opencv", "gaussian blur", "histogram equalization"],
            "Vision Tasks": ["object detection", "yolo", "semantic segmentation", "image classification", "feature matching", "iou"]
        },
        "Generative AI": {
            "LLMs & Prompting": ["large language model", "llm", "rag", "retrieval augmented generation", "prompt engineering", "temperature", "fine-tuning", "lora", "rlhf", "hallucination", "langchain"],
            "Generative Models": ["diffusion models", "gan", "generative adversarial", "stable diffusion", "transformer decoder"]
        },
        "Cloud": {
            "GCP / AWS / Azure": ["aws", "gcp", "azure", "s3", "cloud storage", "ec2", "compute engine", "iam", "vpc", "lambda", "cloud functions", "serverless"],
            "Cloud Architecture": ["scalability", "high availability", "load balancer", "auto scaling", "multi-region", "disaster recovery"]
        },
        "DevOps": {
            "Containers & Orchestration": ["docker", "dockerfile", "container", "kubernetes", "k8s", "pod", "deployment", "helm", "ingress"],
            "CI/CD & Monitoring": ["ci/cd", "github actions", "jenkins", "pipeline", "prometheus", "grafana", "terraform", "infrastructure as code"]
        },
        "Data Analytics": {
            "Analysis & Exploration": ["eda", "exploratory data analysis", "data cleaning", "pandas", "numpy", "matplotlib", "seaborn", "correlation", "data wrangling"],
            "Business Metrics": ["kpi", "churn rate", "cohort analysis", "retention", "conversion rate", "a/b testing"]
        },
        "Power BI": {
            "DAX & Modeling": ["power bi", "dax", "calculated column", "measure", "power query", "star schema", "data modeling", "bi dashboard", "powerbi"]
        },
        "Excel": {
            "Formulas & Tables": ["excel", "vlookup", "xlookup", "pivot table", "index match", "conditional formatting", "sumifs", "countifs", "spreadsheet"]
        },
        "Web Development": {
            "Frontend & Backend": ["react", "vue", "angular", "node.js", "express", "html5", "css3", "rest api", "graphql", "dom", "jwt", "cors", "state management", "redux"]
        },
        "System Design": {
            "Distributed Systems": ["system design", "microservices", "caching", "redis", "cdn", "kafka", "message queue", "sharding", "replication", "cap theorem", "consistent hashing", "rate limiting"]
        },
        "HR": {
            "General HR": ["tell me about yourself", "why should we hire you", "where do you see yourself in 5 years", "salary expectations", "strengths and weaknesses", "why this company"]
        },
        "Behavioral": {
            "STAR Method": ["star method", "tell me about a time", "conflict with teammate", "handled failure", "leadership experience", "tight deadline", "disagreement with manager"]
        },
        "Communication": {
            "Soft Skills": ["presentation", "client communication", "active listening", "cross-functional collaboration", "negotiation", "articulation"]
        },
        "Project": {
            "Project Discussion": ["describe your major project", "architecture of your project", "challenges faced in project", "tech stack choices", "trade-offs made", "project contribution"]
        },
        "Resume": {
            "Resume Walkthrough": ["walk me through your resume", "gap in education", "explain this certification", "coursework", "internship experience", "extracurricular"]
        }
    }

    @classmethod
    def classify(cls, text: str, title: str = "") -> Tuple[str, str, str, List[str]]:
        """
        Classifies given text and title into:
        (category, subcategory, topic, matched_skills)
        """
        combined = f"{title} {text}".lower()

        scores: Dict[str, float] = {cat: 0.0 for cat in SUPPORTED_TAXONOMIES}
        subcat_matches: Dict[str, Dict[str, int]] = {}
        matched_skills_by_cat: Dict[str, List[str]] = {cat: [] for cat in SUPPORTED_TAXONOMIES}

        for cat, subcats in cls.TAXONOMY_KEYWORDS.items():
            subcat_matches[cat] = {}
            for subcat, keywords in subcats.items():
                count = 0
                for kw in keywords:
                    # Look for exact word or phrase boundary
                    pattern = r"\b" + re.escape(kw) + r"\b"
                    matches = len(re.findall(pattern, combined))
                    if matches > 0:
                        count += matches
                        scores[cat] += matches * (3.0 if kw in title.lower() else 1.0)
                        matched_skills_by_cat[cat].append(kw.title())
                subcat_matches[cat][subcat] = count

        # Pick highest scoring category
        best_cat = max(scores, key=scores.get)

        # Fallback if no keywords matched
        if scores[best_cat] == 0:
            if "?" in text and any(w in combined for w in ["what", "why", "how", "explain", "describe"]):
                best_cat = "Programming"
            else:
                best_cat = "DSA"

        # Determine subcategory and topic
        subcats_for_best = subcat_matches.get(best_cat, {})
        if subcats_for_best and max(subcats_for_best.values(), default=0) > 0:
            best_subcat = max(subcats_for_best, key=subcats_for_best.get)
        else:
            first_subcat = list(cls.TAXONOMY_KEYWORDS.get(best_cat, {"General": []}).keys())[0]
            best_subcat = first_subcat

        # Topic: first matched skill or title-based topic
        matched_skills = matched_skills_by_cat.get(best_cat, [])
        best_topic = matched_skills[0] if matched_skills else best_subcat

        return best_cat, best_subcat, best_topic, matched_skills[:6]
