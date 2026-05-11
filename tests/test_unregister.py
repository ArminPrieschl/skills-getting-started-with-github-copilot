import pytest


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes participant from activity"""
    email = "michael@mergington.edu"
    
    # Verify participant exists
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
    
    # Unregister
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_decreases_participant_count(client):
    """Test that unregister decreases the participant count"""
    # Get initial count
    response = client.get("/activities")
    activities = response.json()
    initial_count = len(activities["Chess Club"]["participants"])
    
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Get new count
    response = client.get("/activities")
    activities = response.json()
    new_count = len(activities["Chess Club"]["participants"])
    
    assert new_count == initial_count - 1


def test_unregister_nonexistent_activity(client):
    """Test unregister from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_not_registered_student(client):
    """Test that unregistering non-registered student returns 400"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not registered for this activity"


def test_unregister_preserves_other_participants(client):
    """Test that unregistering one student doesn't affect others"""
    # Get initial participants
    response = client.get("/activities")
    activities = response.json()
    initial_participants = activities["Chess Club"]["participants"].copy()
    
    email_to_remove = "michael@mergington.edu"
    
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email_to_remove}
    )
    
    # Get updated participants
    response = client.get("/activities")
    activities = response.json()
    updated_participants = activities["Chess Club"]["participants"]
    
    # Verify removed email is gone
    assert email_to_remove not in updated_participants
    
    # Verify other participants are still there
    for participant in initial_participants:
        if participant != email_to_remove:
            assert participant in updated_participants


def test_signup_after_unregister(client):
    """Test that student can signup again after unregistering"""
    email = "michael@mergington.edu"
    
    # Unregister
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Signup again
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify signup worked
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]


def test_unregister_last_participant(client):
    """Test unregistering the last participant from an activity"""
    # Get an activity with only one participant
    response = client.get("/activities")
    activities = response.json()
    art_studio = activities["Art Studio"]
    
    # Should have only one participant
    assert len(art_studio["participants"]) == 1
    only_participant = art_studio["participants"][0]
    
    # Unregister the only participant
    response = client.delete(
        "/activities/Art Studio/unregister",
        params={"email": only_participant}
    )
    assert response.status_code == 200
    
    # Verify activity now has no participants
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Art Studio"]["participants"]) == 0
