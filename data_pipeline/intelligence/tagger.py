"""
Company & Role Tagger.
Extracts and tags verified hiring companies and target engineering/analytics roles
from question context, historical placement test patterns, and interview metadata.
"""

import re
from typing import List, Tuple, Set


class EntityTagger:
    """Extracts company and role tags with case normalization and deduplication."""

    KNOWN_COMPANIES = {
        "google": "Google",
        "amazon": "Amazon",
        "microsoft": "Microsoft",
        "meta": "Meta",
        "facebook": "Meta",
        "apple": "Apple",
        "netflix": "Netflix",
        "uber": "Uber",
        "goldman sachs": "Goldman Sachs",
        "morgan stanley": "Morgan Stanley",
        "jp morgan": "JPMorgan Chase",
        "jpmorgan": "JPMorgan Chase",
        "adobe": "Adobe",
        "salesforce": "Salesforce",
        "oracle": "Oracle",
        "cisco": "Cisco",
        "atlassian": "Atlassian",
        "flipkart": "Flipkart",
        "swiggy": "Swiggy",
        "zomato": "Zomato",
        "tcs": "TCS",
        "infosys": "Infosys",
        "wipro": "Wipro",
        "accenture": "Accenture",
        "cognizant": "Cognizant",
        "capgemini": "Capgemini",
        "hcl": "HCLTech",
        "walmart": "Walmart Labs",
        "qualcomm": "Qualcomm",
        "intel": "Intel",
        "nvidia": "NVIDIA",
        "deloitte": "Deloitte",
        "ey": "EY",
        "pwc": "PwC",
        "kpmg": "KPMG",
    }

    KNOWN_ROLES = {
        "sde": "SDE-1",
        "sde 1": "SDE-1",
        "sde-1": "SDE-1",
        "sde 2": "SDE-2",
        "software engineer": "Software Engineer",
        "software developer": "Software Engineer",
        "backend developer": "Backend Engineer",
        "backend engineer": "Backend Engineer",
        "frontend developer": "Frontend Engineer",
        "frontend engineer": "Frontend Engineer",
        "full stack": "Full Stack Developer",
        "full stack developer": "Full Stack Developer",
        "data analyst": "Data Analyst",
        "business analyst": "Business Analyst",
        "data scientist": "Data Scientist",
        "ml engineer": "Machine Learning Engineer",
        "machine learning engineer": "Machine Learning Engineer",
        "ai engineer": "AI Engineer",
        "cloud engineer": "Cloud Engineer",
        "devops engineer": "DevOps Engineer",
        "qa engineer": "QA / SDET",
        "sdet": "QA / SDET",
        "system engineer": "Systems Engineer",
    }

    # Default company & role distributions by taxonomy if none are explicitly present
    CATEGORY_DEFAULTS = {
        "DSA": (["Google", "Amazon", "Microsoft"], ["SDE-1", "Software Engineer"]),
        "SQL": (["Amazon", "Flipkart", "Deloitte"], ["Data Analyst", "Backend Engineer"]),
        "DBMS": (["Oracle", "Microsoft", "TCS"], ["Software Engineer", "Backend Engineer"]),
        "OS": (["Qualcomm", "Intel", "Cisco"], ["Systems Engineer", "Software Engineer"]),
        "Computer Networks": (["Cisco", "Amazon", "Infosys"], ["Systems Engineer", "Cloud Engineer"]),
        "OOP": (["TCS", "Infosys", "Accenture"], ["Software Engineer", "Full Stack Developer"]),
        "Programming": (["Amazon", "Microsoft", "Accenture"], ["Software Engineer", "SDE-1"]),
        "Aptitude": (["TCS", "Cognizant", "Accenture", "Infosys"], ["Associate Software Engineer", "Graduate Trainee"]),
        "AI": (["Google", "Microsoft", "NVIDIA"], ["AI Engineer", "Data Scientist"]),
        "ML": (["Amazon", "Meta", "Walmart Labs"], ["Machine Learning Engineer", "Data Scientist"]),
        "DL": (["NVIDIA", "Google", "Apple"], ["AI Engineer", "Computer Vision Engineer"]),
        "NLP": (["Google", "Microsoft", "Amazon"], ["NLP Engineer", "AI Engineer"]),
        "Computer Vision": (["NVIDIA", "Qualcomm", "Apple"], ["Computer Vision Engineer", "AI Engineer"]),
        "Generative AI": (["Google", "Microsoft", "Meta"], ["Generative AI Engineer", "AI Researcher"]),
        "Cloud": (["Amazon", "Microsoft", "Google"], ["Cloud Engineer", "DevOps Engineer"]),
        "DevOps": (["Atlassian", "Adobe", "Netflix"], ["DevOps Engineer", "Site Reliability Engineer"]),
        "Data Analytics": (["Deloitte", "EY", "Amazon"], ["Data Analyst", "Business Analyst"]),
        "Power BI": (["Deloitte", "PwC", "Accenture"], ["Power BI Developer", "Business Intelligence Analyst"]),
        "Excel": (["EY", "KPMG", "PwC"], ["Financial Analyst", "Data Analyst"]),
        "Web Development": (["Swiggy", "Zomato", "Uber"], ["Frontend Engineer", "Full Stack Developer"]),
        "System Design": (["Uber", "Meta", "Google"], ["SDE-2", "Backend Engineer"]),
        "HR": (["Amazon", "Google", "TCS"], ["All Roles"]),
        "Behavioral": (["Amazon", "Microsoft", "Google"], ["All Roles"]),
        "Communication": (["Deloitte", "Accenture", "Infosys"], ["All Roles"]),
        "Project": (["Google", "Amazon", "Microsoft"], ["Software Engineer", "SDE-1"]),
        "Resume": (["Google", "Amazon", "TCS"], ["All Roles"]),
    }

    @classmethod
    def tag_companies_and_roles(cls, text: str, category: str, existing_companies: List[str] = None, existing_roles: List[str] = None) -> Tuple[List[str], List[str]]:
        """
        Extracts verified companies and roles from text and existing metadata.
        Falls back to curated industry standard distributions if empty.
        """
        lower_text = text.lower()
        extracted_companies: Set[str] = set()
        extracted_roles: Set[str] = set()

        # Add pre-existing tags
        if existing_companies:
            for c in existing_companies:
                if c.strip():
                    extracted_companies.add(c.strip())

        if existing_roles:
            for r in existing_roles:
                if r.strip():
                    extracted_roles.add(r.strip())

        # Match known companies in text
        for needle, canonical in cls.KNOWN_COMPANIES.items():
            pattern = r"\b" + re.escape(needle) + r"\b"
            if re.search(pattern, lower_text):
                extracted_companies.add(canonical)

        # Match known roles in text
        for needle, canonical in cls.KNOWN_ROLES.items():
            pattern = r"\b" + re.escape(needle) + r"\b"
            if re.search(pattern, lower_text):
                extracted_roles.add(canonical)

        # Apply category defaults if still empty
        if not extracted_companies:
            defaults = cls.CATEGORY_DEFAULTS.get(category, (["Tech Companies"], ["Software Engineer"]))
            extracted_companies.update(defaults[0])

        if not extracted_roles:
            defaults = cls.CATEGORY_DEFAULTS.get(category, (["Tech Companies"], ["Software Engineer"]))
            extracted_roles.update(defaults[1])

        return sorted(list(extracted_companies)), sorted(list(extracted_roles))
