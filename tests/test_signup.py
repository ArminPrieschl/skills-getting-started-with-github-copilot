import pytest


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds participant to the activity"""
    new_email = "newstudent@mergington.edu"
    
    # Signup
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": new_email}
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    assert new_email in activities["Chess Club"]["participants"]


def test_signup_increases_participant_count(client):
    """Test that signup increases the participant count"""
    # Get initial count
    response = client.get("/activities")
    activities = response.json()
    initial_count = len(activities["Chess Club"]["participants"])
    
    # Signup
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    # Get new count
    response = client.get("/activities")
    activities = response.json()
    new_count = len(activities["Chess Club"]["participants"])
    
    assert new_count == initial_count + 1


def test_signup_nonexistent_activity(client):
    """Test signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_fails(client):
    """Test that duplicate signup returns 400 error"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up"


def test_signup_multiple_activities(client):
    """Test that same student can signup for multiple activities"""
    email = "newstudent@mergington.edu"
    
    # Signup for first activity
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Signup for second activity
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups succeeded
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_preserves_existing_participants(client):
    """Test that new signup doesn't remove existing participants"""
    # Get initial participants
    response = client.get("/activities")
    activities = response.json()
    initial_participants = activities["Math Club"]["participants"].copy()
    
    # Signup new participant
    new_email = "newstudent@mergington.edu"
    client.post(
        "/activities/Math Club/signup",
        params={"email": new_email}
    )
    
    # Get updated participants
    response = client.get("/activities")
    activities = response.json()
    updated_participants = activities["Math Club"]["participants"]
    
    # Verify all initial participants are still there
    for participant in initial_participants:
        assert participant in updated_participants
    
    # And new participant was added
    assert new_email in updated_participants
