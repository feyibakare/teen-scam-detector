import database
from scam_detector import analyze_message, HIGH


def fresh_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_FILE", str(tmp_path / "test.db"))
    database.init_db()
    database.create_user("alice", "hash-a")
    database.create_user("bob", "hash-b")
    return database.get_user("alice")["id"], database.get_user("bob")["id"]


def test_save_and_read_scan(tmp_path, monkeypatch):
    alice, bob = fresh_db(tmp_path, monkeypatch)
    message = "URGENT! You won a free iPhone! Click here now!"
    database.save_scan(alice, message, analyze_message(message))

    history = database.get_history(alice)
    assert len(history) == 1
    assert history[0]["level"] == HIGH
    assert history[0]["message"] == message


def test_users_only_see_their_own_scans(tmp_path, monkeypatch):
    alice, bob = fresh_db(tmp_path, monkeypatch)
    database.save_scan(alice, "hello", analyze_message("hello"))
    assert len(database.get_history(alice)) == 1
    assert database.get_history(bob) == []


def test_cannot_bookmark_or_delete_someone_elses_scan(tmp_path, monkeypatch):
    alice, bob = fresh_db(tmp_path, monkeypatch)
    database.save_scan(alice, "hello", analyze_message("hello"))
    scan_id = database.get_history(alice)[0]["id"]

    database.toggle_bookmark(bob, scan_id)
    assert database.get_history(alice)[0]["bookmarked"] == 0

    database.delete_scan(bob, scan_id)
    assert len(database.get_history(alice)) == 1


def test_bookmark_and_delete_own_scan(tmp_path, monkeypatch):
    alice, bob = fresh_db(tmp_path, monkeypatch)
    database.save_scan(alice, "hello", analyze_message("hello"))
    scan_id = database.get_history(alice)[0]["id"]

    database.toggle_bookmark(alice, scan_id)
    assert database.get_history(alice)[0]["bookmarked"] == 1
    database.toggle_bookmark(alice, scan_id)
    assert database.get_history(alice)[0]["bookmarked"] == 0

    database.delete_scan(alice, scan_id)
    assert database.get_history(alice) == []


def test_delete_all_only_affects_that_user(tmp_path, monkeypatch):
    alice, bob = fresh_db(tmp_path, monkeypatch)
    database.save_scan(alice, "hello", analyze_message("hello"))
    database.save_scan(bob, "hi there", analyze_message("hi there"))

    database.delete_all_scans(alice)
    assert database.get_history(alice) == []
    assert len(database.get_history(bob)) == 1
