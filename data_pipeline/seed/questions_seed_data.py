"""
Realistic Seed Question Bank for Placement OS.
Contains comprehensive, high-quality question items across all required categories:
DSA, SQL, Aptitude, OOP, DBMS, OS, Computer Networks, Python, Java, JavaScript,
AI/ML, Data Analytics, Power BI, Excel, System Design, Web Development, HR, Project, Resume.

Designed so the demo dashboard looks vibrant, realistic, and production-ready.
"""

from typing import List, Dict, Any

SEED_QUESTIONS: List[Dict[str, Any]] = [
    # ------------------ DSA ------------------
    {
        "title": "0/1 Knapsack Problem",
        "category": "DSA",
        "subcategory": "Dynamic Programming",
        "topic": "Knapsack",
        "skills": ["Dynamic Programming", "0/1 Knapsack", "Recursion", "Memoization"],
        "question_type": "Coding",
        "difficulty": "Medium",
        "companies": ["Google", "Amazon", "Microsoft", "Flipkart"],
        "roles": ["SDE-1", "Software Engineer"],
        "observed_frequency": 14,
        "source_count": 4,
        "problem_statement": "Given weights and values of N items, put these items in a knapsack of capacity W to get the maximum total value in the knapsack. Each item can either be selected entirely or not at all (0-1 property). Return the maximum value achievable.",
        "solution_approach": "Use 2D Dynamic Programming where dp[i][w] represents maximum value using first i items with knapsack capacity w. Transition: dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]]) if wt[i-1] <= w else dp[i-1][w]. Can be space-optimized to a 1D array of size W+1 by iterating backwards.",
        "learning_hints": [
            "Consider the binary choice for each item: include it or exclude it.",
            "If you include an item, what happens to the remaining knapsack capacity?",
            "Can you optimize the 2D DP table O(N*W) space into a single 1D row by iterating right-to-left?"
        ],
        "test_cases": [
            {"input": "W = 4, val = [1, 2, 3], wt = [4, 5, 1]", "expected_output": "3", "is_hidden": False, "explanation": "Pick item 3 with wt=1 and val=3."},
            {"input": "W = 3, val = [1, 2, 3], wt = [4, 5, 6]", "expected_output": "0", "is_hidden": True, "explanation": "No item fits in capacity."}
        ]
    },
    {
        "title": "Trapping Rain Water",
        "category": "DSA",
        "subcategory": "Arrays & Hashing",
        "topic": "Two Pointer",
        "skills": ["Two Pointer", "Arrays", "Monotonic Stack"],
        "question_type": "Coding",
        "difficulty": "Hard",
        "companies": ["Google", "Amazon", "Goldman Sachs"],
        "roles": ["SDE-1", "SDE-2"],
        "observed_frequency": 19,
        "source_count": 5,
        "problem_statement": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "solution_approach": "Optimal approach utilizes two pointers (left and right) keeping track of max_left and max_right. Water trapped at any index is min(max_left, max_right) - height[i]. Time complexity: O(N), Space complexity: O(1).",
        "learning_hints": [
            "What determines the water trapped above bar i? The minimum of maximum height to its left and right minus its own height.",
            "Can you avoid storing prefix and suffix maximums using two pointers moving inwards?"
        ],
        "test_cases": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "expected_output": "6", "is_hidden": False, "explanation": "6 units of rain water trapped."},
            {"input": "height = [4,2,0,3,2,5]", "expected_output": "9", "is_hidden": True, "explanation": "9 units of water trapped."}
        ]
    },
    {
        "title": "Reverse Linked List in K-Group",
        "category": "DSA",
        "subcategory": "Linked Lists",
        "topic": "Reversal",
        "skills": ["Linked Lists", "Pointers", "Recursion"],
        "question_type": "Coding",
        "difficulty": "Hard",
        "companies": ["Microsoft", "Amazon", "Meta"],
        "roles": ["SDE-1", "Software Engineer"],
        "observed_frequency": 11,
        "source_count": 3,
        "problem_statement": "Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list. If the number of nodes is not a multiple of k, left-out nodes at the end should remain as-is.",
        "solution_approach": "Check if at least k nodes exist from current node. If yes, reverse those k nodes iteratively and recursively connect the tail of this reversed group to the result of reversing the next k nodes.",
        "learning_hints": [
            "First verify if there are k nodes remaining before attempting to reverse.",
            "Standard linked list 3-pointer reversal (prev, curr, next) works for each group of k."
        ],
        "test_cases": [
            {"input": "head = [1,2,3,4,5], k = 2", "expected_output": "[2,1,4,3,5]", "is_hidden": False, "explanation": "Nodes 1-2 and 3-4 are reversed; 5 remains."},
            {"input": "head = [1,2,3,4,5], k = 3", "expected_output": "[3,2,1,4,5]", "is_hidden": True, "explanation": "Nodes 1-3 reversed; 4-5 remain."}
        ]
    },

    # ------------------ SQL ------------------
    {
        "title": "Department Top Three Salaries",
        "category": "SQL",
        "subcategory": "Window Functions",
        "topic": "Dense Rank",
        "skills": ["SQL", "Window Functions", "DENSE_RANK", "Joins"],
        "question_type": "Coding",
        "difficulty": "Hard",
        "companies": ["Amazon", "Flipkart", "Uber", "Oracle"],
        "roles": ["Data Analyst", "Backend Engineer"],
        "observed_frequency": 16,
        "source_count": 4,
        "problem_statement": "A company's executives are interested in seeing who earns the most money in each of the company's departments. A high earner in a department is an employee who has a salary in the top three unique salaries for that department. Write a solution to find the employees who are high earners in each of the departments.",
        "solution_approach": "Use DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) as salary_rank in a Common Table Expression (CTE). Filter WHERE salary_rank <= 3 and INNER JOIN with Department table.",
        "learning_hints": [
            "Why is DENSE_RANK preferred over RANK or ROW_NUMBER here? Because top 3 UNIQUE salaries are required.",
            "Use a CTE or subquery because window functions cannot be directly filtered in the WHERE clause."
        ],
        "test_cases": [
            {"input": "Employee: [[1, 'Joe', 85000, 1], [2, 'Henry', 80000, 2], [3, 'Sam', 60000, 2], [4, 'Max', 90000, 1]], Department: [[1, 'IT'], [2, 'Sales']]", "expected_output": "IT: Max (90k), Joe (85k); Sales: Henry (80k), Sam (60k)", "is_hidden": False}
        ]
    },
    {
        "title": "Second Highest Salary",
        "category": "SQL",
        "subcategory": "Queries & Joins",
        "topic": "Subqueries",
        "skills": ["SQL", "Subquery", "DENSE_RANK", "LIMIT OFFSET"],
        "question_type": "Coding",
        "difficulty": "Medium",
        "companies": ["Amazon", "TCS", "Cognizant", "Infosys"],
        "roles": ["Data Analyst", "Software Engineer"],
        "observed_frequency": 22,
        "source_count": 6,
        "problem_statement": "Write a SQL query to report the second highest distinct salary from the Employee table. If there is no second highest salary, the query should report null.",
        "solution_approach": "SELECT MAX(salary) AS SecondHighestSalary FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee); Or use IFNULL((SELECT DISTINCT salary FROM Employee ORDER BY salary DESC LIMIT 1 OFFSET 1), NULL).",
        "learning_hints": [
            "Make sure to handle duplicates with DISTINCT.",
            "Ensure the query returns NULL (and not an empty row) when fewer than 2 distinct salaries exist."
        ],
        "test_cases": [
            {"input": "Employee: [[1, 100], [2, 200], [3, 300]]", "expected_output": "200", "is_hidden": False},
            {"input": "Employee: [[1, 100]]", "expected_output": "null", "is_hidden": True}
        ]
    },

    # ------------------ DBMS ------------------
    {
        "title": "Explain ACID Properties and WAL Protocol",
        "category": "DBMS",
        "subcategory": "Transactions & Concurrency",
        "topic": "ACID Properties",
        "skills": ["DBMS", "Transactions", "ACID", "WAL", "Concurrency"],
        "question_type": "Subjective",
        "difficulty": "Easy",
        "companies": ["Oracle", "Microsoft", "TCS", "Infosys"],
        "roles": ["Software Engineer", "Backend Engineer"],
        "observed_frequency": 18,
        "source_count": 5,
        "problem_statement": "Explain the four ACID properties in relational database management systems. How does Write-Ahead Logging (WAL) ensure Atomicity and Durability during unexpected system crashes?",
        "solution_approach": "1. Atomicity: All or nothing execution (via undo logs).\n2. Consistency: Database transitions from one valid state to another satisfying all integrity constraints.\n3. Isolation: Concurrent transactions do not interfere (isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable).\n4. Durability: Committed transactions persist permanently.\nWAL rule: Redo and undo log entries must be flushed to non-volatile storage before corresponding dirty data pages are written to disk.",
        "learning_hints": [
            "Structure your answer around each letter of ACID with concrete examples.",
            "For WAL, remember the core invariant: log record to disk before data block to disk."
        ]
    },
    {
        "title": "Database Normalization: 1NF to BCNF",
        "category": "DBMS",
        "subcategory": "Normalization",
        "topic": "Boyce-Codd Normal Form",
        "skills": ["DBMS", "Normalization", "Functional Dependencies", "Keys"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Oracle", "Amazon", "Wipro"],
        "roles": ["Software Engineer", "Database Administrator"],
        "observed_frequency": 12,
        "source_count": 3,
        "problem_statement": "Define 1NF, 2NF, 3NF, and BCNF. Provide a scenario where a relation is in 3NF but violates BCNF, and demonstrate the lossless decomposition.",
        "solution_approach": "1NF: Atomic values; 2NF: 1NF + no partial dependency; 3NF: 2NF + no transitive dependency (for X->A, X is superkey or A is prime attribute); BCNF: for every non-trivial functional dependency X->A, X must strictly be a superkey.",
        "learning_hints": [
            "Remember that 3NF allows A to be a prime attribute even if X is not a superkey; BCNF removes this relaxation."
        ]
    },

    # ------------------ OS ------------------
    {
        "title": "Virtual Memory and Paging Mechanism",
        "category": "OS",
        "subcategory": "Memory Management",
        "topic": "Virtual Memory",
        "skills": ["OS", "Virtual Memory", "Paging", "TLB", "Page Faults"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Qualcomm", "Intel", "Cisco", "NVIDIA"],
        "roles": ["Systems Engineer", "Software Engineer"],
        "observed_frequency": 15,
        "source_count": 4,
        "problem_statement": "Describe how Virtual Memory is implemented using paging. Walk through the address translation process from Virtual Address to Physical Address via the Translation Lookaside Buffer (TLB) and multi-level page tables, and explain how a page fault is handled by the OS kernel.",
        "solution_approach": "Virtual address split into Page Number and Offset. CPU checks TLB: if TLB hit, physical frame obtained immediately. If TLB miss, MMU walks page tables. If valid bit is 0, a page fault trap occurs: OS locates page on swap space, finds free frame (or evicts using LRU/Clock algorithm), loads page, updates page table, and restarts faulting instruction.",
        "learning_hints": [
            "Differentiate between a TLB hit/miss and a Page Table valid/invalid bit check.",
            "Mention the exact steps the OS takes during the page fault ISR (interrupt service routine)."
        ]
    },

    # ------------------ Computer Networks ------------------
    {
        "title": "TCP 3-Way Handshake and 4-Way Termination",
        "category": "Computer Networks",
        "subcategory": "OSI & TCP/IP",
        "topic": "TCP Handshake",
        "skills": ["Computer Networks", "TCP/IP", "Transport Layer", "Reliability"],
        "question_type": "Subjective",
        "difficulty": "Easy",
        "companies": ["Cisco", "Amazon", "Infosys", "Swiggy"],
        "roles": ["Cloud Engineer", "Systems Engineer", "Backend Engineer"],
        "observed_frequency": 20,
        "source_count": 5,
        "problem_statement": "Explain the TCP Three-Way Handshake used to establish a reliable connection, and the Four-Way Handshake used for graceful connection termination. What is the purpose of the TIME_WAIT state?",
        "solution_approach": "Handshake: Client sends SYN(seq=x) -> Server replies SYN(seq=y)+ACK(ack=x+1) -> Client sends ACK(ack=y+1). Termination: Client sends FIN -> Server sends ACK -> Server sends FIN -> Client sends ACK. TIME_WAIT (typically 2*MSL) ensures delayed packets in transit drain and the final ACK is received by the server.",
        "learning_hints": [
            "Draw or trace the sequence numbers and ACK numbers in each packet.",
            "Explain why 2 MSL (Maximum Segment Lifetime) is needed in TIME_WAIT."
        ]
    },

    # ------------------ OOP ------------------
    {
        "title": "SOLID Design Principles with Code Examples",
        "category": "OOP",
        "subcategory": "Design Principles",
        "topic": "SOLID Principles",
        "skills": ["OOP", "SOLID", "Software Architecture", "Clean Code"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Amazon", "Microsoft", "TCS", "Accenture"],
        "roles": ["Software Engineer", "Full Stack Developer"],
        "observed_frequency": 17,
        "source_count": 4,
        "problem_statement": "Define each of the 5 SOLID design principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion. Give a concise code violation and fix for Liskov Substitution Principle (LSP).",
        "solution_approach": "Classic LSP violation: Square inheriting from Rectangle where setWidth changes height. Fix: Extract common Shape interface or make Rectangle and Square independent implementations.",
        "learning_hints": [
            "Remember that LSP states derived classes must be substitutable for their base classes without altering program correctness."
        ]
    },

    # ------------------ Programming: Python ------------------
    {
        "title": "Python Generators and Memory Efficiency",
        "category": "Programming",
        "subcategory": "Python",
        "topic": "Generators",
        "skills": ["Python", "Generators", "Iterators", "Memory Management"],
        "question_type": "Coding",
        "difficulty": "Medium",
        "companies": ["Amazon", "Google", "Walmart Labs"],
        "roles": ["Backend Engineer", "Data Engineer", "Software Engineer"],
        "observed_frequency": 13,
        "source_count": 3,
        "problem_statement": "Write a Python generator function `read_large_file(file_path, chunk_size)` that streams a multi-gigabyte log file in fixed chunks using `yield` without loading the full file into RAM. Explain how generators maintain execution state using generator frames.",
        "solution_approach": "Open file in context manager, read chunk_size bytes inside a while loop, yield chunk until empty string. The generator function returns a generator object pausing at yield and preserving local variable state.",
        "learning_hints": [
            "Use `while True` with `f.read(chunk_size)` and break when data is empty.",
            "Generators implement the Python iterator protocol (`__iter__` and `__next__`)."
        ],
        "test_cases": [
            {"input": "chunk_size=1024", "expected_output": "generator yields 1024-byte chunks", "is_hidden": False}
        ]
    },

    # ------------------ Programming: Java ------------------
    {
        "title": "Java Garbage Collection and JVM Memory Model",
        "category": "Programming",
        "subcategory": "Java",
        "topic": "JVM Memory",
        "skills": ["Java", "JVM", "Garbage Collection", "Heap Memory"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Goldman Sachs", "Morgan Stanley", "Oracle", "Infosys"],
        "roles": ["Software Engineer", "Backend Engineer"],
        "observed_frequency": 15,
        "source_count": 4,
        "problem_statement": "Explain the JVM memory model: Heap (Young Generation: Eden, S0, S1, and Old/Tenured Generation), Metaspace, and Stack. How does the G1 Garbage Collector balance throughput and low pause times?",
        "solution_approach": "Objects created in Eden. Surviving minor GC moved to Survivor (S0/S1). After age threshold (tenuring), promoted to Old Gen. G1 GC divides heap into equal regions and prioritizes regions with the most garbage ('Garbage-First') while meeting user-specified pause time targets.",
        "learning_hints": [
            "Contrast Java Heap memory (shared across threads) with Java Thread Stack (isolated per thread)."
        ]
    },

    # ------------------ Programming: JavaScript ------------------
    {
        "title": "JavaScript Event Loop and Microtask Queue",
        "category": "Programming",
        "subcategory": "JavaScript",
        "topic": "Event Loop",
        "skills": ["JavaScript", "Event Loop", "Promises", "Async"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Uber", "Swiggy", "Zomato", "Flipkart"],
        "roles": ["Frontend Engineer", "Full Stack Developer"],
        "observed_frequency": 16,
        "source_count": 4,
        "problem_statement": "Explain the order of execution between Call Stack, Web APIs, Microtask Queue (Promises, queueMicrotask, MutationObserver), and Macrotask / Callback Queue (setTimeout, setInterval). What is the output of:\nconsole.log(1);\nsetTimeout(() => console.log(2), 0);\nPromise.resolve().then(() => console.log(3));\nconsole.log(4);",
        "solution_approach": "Output is: 1, 4, 3, 2. Synchronous code executes first (1, 4). Microtasks are drained completely before the next macrotask runs, so Promise callback (3) executes next. Finally, setTimeout callback in macrotask queue executes (2).",
        "learning_hints": [
            "Microtasks always have higher priority than macrotasks.",
            "All pending microtasks are flushed after every synchronous call stack turn."
        ]
    },

    # ------------------ Aptitude ------------------
    {
        "title": "Speed, Time, and Distance: Trains Crossing",
        "category": "Aptitude",
        "subcategory": "Quantitative",
        "topic": "Relative Speed",
        "skills": ["Quantitative Aptitude", "Relative Speed", "Arithmetic"],
        "question_type": "MCQ",
        "difficulty": "Easy",
        "companies": ["TCS", "Accenture", "Cognizant", "Capgemini"],
        "roles": ["Graduate Trainee", "Associate Software Engineer"],
        "observed_frequency": 25,
        "source_count": 7,
        "problem_statement": "Two trains 140 m and 160 m long run at the speeds of 60 km/hr and 40 km/hr respectively in opposite directions on parallel tracks. What is the time (in seconds) taken for them to clear each other from the moment they meet?",
        "options": ["9 seconds", "10.8 seconds", "12 seconds", "14.4 seconds"],
        "correct_answer": "10.8 seconds",
        "solution_approach": "Total distance = 140 + 160 = 300 m. Relative speed in opposite direction = 60 + 40 = 100 km/hr = 100 * (5/18) = 250/9 m/s. Time = Distance / Speed = 300 / (250/9) = 300 * 9 / 250 = 10.8 seconds.",
        "learning_hints": [
            "When moving in opposite directions, relative speed is the sum of both speeds.",
            "Convert km/hr to m/s by multiplying by 5/18."
        ]
    },

    # ------------------ AI / ML ------------------
    {
        "title": "Bias-Variance Tradeoff and Model Generalization",
        "category": "ML",
        "subcategory": "Supervised Learning",
        "topic": "Bias Variance",
        "skills": ["Machine Learning", "Model Evaluation", "Overfitting", "Cross Validation"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Google", "Amazon", "Meta", "Walmart Labs"],
        "roles": ["Machine Learning Engineer", "Data Scientist"],
        "observed_frequency": 14,
        "source_count": 4,
        "problem_statement": "Explain the Bias-Variance Tradeoff in machine learning. How do high bias and high variance manifest in training vs validation errors, and what techniques reduce each?",
        "solution_approach": "Expected test error = Bias^2 + Variance + Irreducible Error. High bias (underfitting): high train and validation error -> fix by increasing model capacity, adding features, reducing regularization. High variance (overfitting): low train error but high validation error -> fix by adding data, feature selection, regularization (L1/L2), dropout, ensemble methods (bagging/Random Forests).",
        "learning_hints": [
            "Relate bias to model assumptions and variance to sensitivity to training fluctuations."
        ]
    },

    # ------------------ Data Analytics ------------------
    {
        "title": "Customer Cohort Retention Analysis",
        "category": "Data Analytics",
        "subcategory": "Analysis & Exploration",
        "topic": "Cohort Analysis",
        "skills": ["Data Analytics", "Pandas", "Cohort Analysis", "Retention", "KPIs"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Amazon", "Swiggy", "Deloitte", "EY"],
        "roles": ["Data Analyst", "Business Analyst"],
        "observed_frequency": 11,
        "source_count": 3,
        "problem_statement": "Explain how you would calculate and interpret a Monthly Customer Retention Cohort Table using transaction records in Python/Pandas or SQL. What key insights does cohort retention reveal compared to aggregate active user metrics?",
        "solution_approach": "1. Identify customer's first purchase month (CohortMonth).\n2. Tag each transaction with TransactionMonth.\n3. Compute CohortIndex = (TransactionYear - CohortYear)*12 + (TransactionMonth - CohortMonth).\n4. Pivot data: rows = CohortMonth, columns = CohortIndex, values = count of unique customer IDs divided by initial cohort size. Reveals product market fit and long-term user decay curves.",
        "learning_hints": [
            "Explain why aggregate monthly active users (MAU) can hide high user churn if top-of-funnel acquisition is artificially high."
        ]
    },

    # ------------------ Power BI ------------------
    {
        "title": "DAX Calculated Columns vs Measures in Power BI",
        "category": "Power BI",
        "subcategory": "DAX & Modeling",
        "topic": "DAX Context",
        "skills": ["Power BI", "DAX", "Row Context", "Filter Context", "Data Modeling"],
        "question_type": "Subjective",
        "difficulty": "Easy",
        "companies": ["Deloitte", "PwC", "Accenture", "KPMG"],
        "roles": ["Power BI Developer", "Business Intelligence Analyst"],
        "observed_frequency": 15,
        "source_count": 4,
        "problem_statement": "What is the critical architectural difference between a Calculated Column and a Measure in Power BI? Detail how Row Context and Filter Context apply to each and discuss RAM memory implications in the VertiPaq engine.",
        "solution_approach": "Calculated Column evaluated at data refresh row-by-row (Row Context), stored in RAM consuming VertiPaq memory. Measure evaluated on-the-fly at query/visualization time based on slicers and user filters (Filter Context), consuming CPU without persistent RAM overhead. Best practice: use Measures whenever aggregation is needed.",
        "learning_hints": [
            "Think about storage: calculated column values exist in RAM permanently; measures calculate dynamically."
        ]
    },

    # ------------------ Excel ------------------
    {
        "title": "INDEX MATCH vs VLOOKUP Performance and Flexibility",
        "category": "Excel",
        "subcategory": "Formulas & Tables",
        "topic": "Lookup Formulas",
        "skills": ["Excel", "INDEX MATCH", "XLOOKUP", "Data Modeling"],
        "question_type": "Subjective",
        "difficulty": "Easy",
        "companies": ["Deloitte", "EY", "KPMG", "PwC"],
        "roles": ["Data Analyst", "Financial Analyst"],
        "observed_frequency": 18,
        "source_count": 5,
        "problem_statement": "Compare INDEX/MATCH and XLOOKUP against traditional VLOOKUP in Microsoft Excel. Why is INDEX/MATCH faster on large enterprise datasets and why does VLOOKUP break when inserting new columns?",
        "solution_approach": "VLOOKUP uses hardcoded column index offsets and requires lookup key to be in the leftmost column. Inserting columns breaks the index reference. INDEX(return_range, MATCH(lookup_value, lookup_range, 0)) decouples rows and columns, allows leftward lookups, and only processes relevant memory vectors.",
        "learning_hints": [
            "Explain what happens to `VLOOKUP(A2, B:E, 3, FALSE)` if a user inserts a new column C."
        ]
    },

    # ------------------ System Design ------------------
    {
        "title": "Design a Distributed Rate Limiter",
        "category": "System Design",
        "subcategory": "Distributed Systems",
        "topic": "Rate Limiting",
        "skills": ["System Design", "Distributed Systems", "Redis", "Token Bucket", "Sliding Window"],
        "question_type": "SystemDesign",
        "difficulty": "Hard",
        "companies": ["Uber", "Google", "Amazon", "Swiggy"],
        "roles": ["SDE-2", "Backend Engineer"],
        "observed_frequency": 14,
        "source_count": 4,
        "problem_statement": "Design a distributed rate limiter capable of enforcing tier-based API throttling (e.g., 100 requests per minute per IP or API key) across a multi-region microservice architecture. Compare the Token Bucket and Sliding Window Log algorithms, and explain how Redis with Lua scripts prevents race conditions.",
        "solution_approach": "Use Redis cluster for centralized fast in-memory counting. Sliding Window Counter combines current and previous window weights. Redis Lua scripts guarantee atomic execution of GET and INCR operations, eliminating race conditions under high concurrent traffic. Add local client memory caching for DDoS shedding.",
        "learning_hints": [
            "Why does a basic Redis `INCR` followed by `EXPIRE` create race conditions?",
            "How do you handle clock drift across servers in distributed rate limiting?"
        ]
    },

    # ------------------ HR & Behavioral ------------------
    {
        "title": "Tell Me About Yourself and Your Career Aspirations",
        "category": "HR",
        "subcategory": "General HR",
        "topic": "Elevator Pitch",
        "skills": ["Communication", "Self Presentation", "Career Alignment"],
        "question_type": "Behavioral",
        "difficulty": "Medium",
        "companies": ["Amazon", "Google", "Microsoft", "TCS", "Infosys"],
        "roles": ["All Roles"],
        "observed_frequency": 30,
        "source_count": 8,
        "problem_statement": "Walk me through your journey: introduce your academic background, core technical focus, top achievements, and explain why you are specifically passionate about joining our organization.",
        "solution_approach": "Use the Present-Past-Future framework:\n1. Present: Current degree, major, and technical passion.\n2. Past: 1-2 key projects, internships, or competitive achievements that demonstrate engineering rigor.\n3. Future: Why this company's scale and engineering culture align with your 3-year growth goals.",
        "learning_hints": [
            "Keep response between 90 and 120 seconds.",
            "Do not merely recite your resume chronologically—focus on impact and enthusiasm."
        ]
    },
    {
        "title": "STAR Method: Handling a High-Pressure Technical Failure",
        "category": "Behavioral",
        "subcategory": "STAR Method",
        "topic": "Overcoming Failure",
        "skills": ["Behavioral", "STAR Method", "Resilience", "Ownership"],
        "question_type": "Behavioral",
        "difficulty": "Medium",
        "companies": ["Amazon", "Microsoft", "Uber"],
        "roles": ["All Roles"],
        "observed_frequency": 21,
        "source_count": 6,
        "problem_statement": "Describe a situation where a technical project or deployment failed or missed a critical deadline. How did you take ownership, communicate with stakeholders, and implement corrective actions?",
        "solution_approach": "Structure response using STAR: Situation (context & stakes), Task (what you were responsible for), Action (root cause analysis, communication, fix implemented), Result (measurable outcome, lessons learned, and preventive systems created).",
        "learning_hints": [
            "Demonstrate extreme ownership: avoid blaming teammates or external circumstances.",
            "Emphasize the post-mortem and what engineering guardrails you implemented."
        ]
    },

    # ------------------ Project & Resume ------------------
    {
        "title": "Deep Dive into Major Technical Project Architecture",
        "category": "Project",
        "subcategory": "Project Discussion",
        "topic": "System Architecture",
        "skills": ["System Architecture", "Tradeoff Analysis", "Project Defense"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["Google", "Amazon", "Microsoft", "Flipkart"],
        "roles": ["Software Engineer", "SDE-1"],
        "observed_frequency": 24,
        "source_count": 7,
        "problem_statement": "Explain the architectural design of your most complex college or internship project. What engineering trade-offs did you make (e.g. database choice, synchronous vs asynchronous communication), what was the bottleneck, and how would you redesign it for 100x traffic?",
        "solution_approach": "State problem being solved -> High-level architecture diagram -> Justify tech stack -> Discuss 1 key bottleneck encountered -> Explain horizontal scaling, caching layer, and asynchronous task workers to achieve 100x scale.",
        "learning_hints": [
            "Interviewers want to see that you understand the trade-offs of the tools you chose, not just that you followed a tutorial."
        ]
    },
    {
        "title": "Resume Deep-Dive: Justifying Skills and Metrics",
        "category": "Resume",
        "subcategory": "Resume Walkthrough",
        "topic": "Resume Defense",
        "skills": ["Resume Verification", "Technical Integrity", "Articulation"],
        "question_type": "Subjective",
        "difficulty": "Medium",
        "companies": ["TCS", "Amazon", "Accenture", "Microsoft"],
        "roles": ["All Roles"],
        "observed_frequency": 26,
        "source_count": 7,
        "problem_statement": "Pick the strongest bullet point on your resume claiming an optimization or metric (e.g. 'Improved latency by 35%'). How did you measure the baseline, what profiling tool did you use, and how did you verify the final improvement?",
        "solution_approach": "Define exact baseline metric -> Explain profiling methodology (e.g. Chrome DevTools, cProfile, benchmark suite) -> Detail specific code/system optimization -> Present post-optimization benchmarks with load test results.",
        "learning_hints": [
            "Every number on your resume is fair game. Never present estimated numbers without knowing the underlying measurement method."
        ]
    }
]
