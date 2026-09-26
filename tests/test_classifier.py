"""
Unit Tests for Taxonomy Classifier and Entity Tagger.
"""

from data_pipeline.intelligence.classifier import TaxonomyClassifier
from data_pipeline.intelligence.tagger import EntityTagger
from data_pipeline.intelligence.difficulty import DifficultyEstimator


def test_taxonomy_classifier():
    # SQL test
    text_sql = "Write a SQL query using inner join and group by to find total department salaries."
    cat, subcat, topic, skills = TaxonomyClassifier.classify(text_sql, "Department Salaries")
    assert cat == "SQL"

    # OS test
    text_os = "Explain virtual memory, paging, and how the TLB translates addresses."
    cat, subcat, topic, skills = TaxonomyClassifier.classify(text_os, "Virtual Memory")
    assert cat == "OS"

    # Power BI test
    text_pbi = "What is the difference between a measure and a calculated column in DAX Power BI?"
    cat, subcat, topic, skills = TaxonomyClassifier.classify(text_pbi, "Power BI DAX")
    assert cat == "Power BI"


def test_entity_tagger():
    text = "This problem was reported in an Amazon and Google SDE-1 interview round."
    companies, roles = EntityTagger.tag_companies_and_roles(text, category="DSA")
    assert "Amazon" in companies
    assert "Google" in companies
    assert "SDE-1" in roles


def test_difficulty_estimator():
    easy_text = "What is an array and how do you loop through it?"
    hard_text = "Implement 0/1 knapsack dynamic programming with memoization and segment tree optimization."
    assert DifficultyEstimator.estimate_difficulty(easy_text, "DSA", "Arrays") == "Easy"
    assert DifficultyEstimator.estimate_difficulty(hard_text, "DSA", "Dynamic Programming") == "Hard"
