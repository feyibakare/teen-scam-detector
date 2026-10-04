import database
from scam_detector import analyze_message, HIGH


def test_bookmark_and_delete(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_FILE", str(tmp_path / "test.db"))
    database.init_db()

    database.save_scan("hello", analyze_message("hello"))
    scan_id = database.get_history()[0]["id"]

    database.toggle_bookmark(scan_id)
    assert database.get_history()[0]["bookmarked"] == 1

    database.toggle_bookmark(scan_id)
    assert database.get_history()[0]["bookmarked"] == 0

    database.delete_scan(scan_id)
    assert database.get_history() == []