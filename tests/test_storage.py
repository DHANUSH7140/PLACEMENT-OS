"""
Unit Tests for Storage Manager and End-to-End Pipeline.
"""

from data_pipeline.storage.storage_manager import StorageManager
from data_pipeline.intelligence.pipeline import QuestionIntelligencePipeline, IngestionItem


def test_storage_validation():
    # Valid resume
    is_valid, err = StorageManager.validate_file("resume.pdf", "resume", file_size=500000)
    assert is_valid is True
    assert err is None

    # Invalid extension for resume
    is_valid, err = StorageManager.validate_file("resume.exe", "resume", file_size=500000)
    assert is_valid is False
    assert "Invalid extension" in err

    # Exceeding size limit
    is_valid, err = StorageManager.validate_file("video.mp4", "resume", file_size=30 * 1024 * 1024)
    assert is_valid is False


def test_pipeline_end_to_end():
    pipeline = QuestionIntelligencePipeline()
    existing_questions = []

    # Process first item
    item1 = IngestionItem(
        raw_text="Explain deadlock conditions: mutual exclusion, hold and wait, no preemption, circular wait in OS.",
        title="Deadlock Conditions",
        source_name="curated_test",
    )
    res1 = pipeline.process_item(item1, existing_questions)
    assert res1["action"] == "INSERTED"
    assert res1["question"].category == "OS"
    assert len(existing_questions) == 1

    # Process identical second item from another source
    item2 = IngestionItem(
        raw_text="Explain deadlock conditions: mutual exclusion, hold and wait, no preemption, circular wait in OS.",
        title="Deadlocks in OS",
        source_name="source_two",
    )
    res2 = pipeline.process_item(item2, existing_questions)
    assert res2["action"] == "MERGED"
    assert res2["question"].observed_frequency == 2
    assert res2["question"].source_count == 2
    assert len(existing_questions) == 1  # No duplicate question created
