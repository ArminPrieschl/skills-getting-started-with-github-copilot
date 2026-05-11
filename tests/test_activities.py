import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Should have 9 activities
    assert len(activities) == 9
    
    # Check that all activity names are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Math Club",
        "Debate Team",
        "Drama Club",
        "Art Studio",
        "Gym Class",
        "Tennis Club",
        "Basketball Team"
    ]
    
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_has_correct_structure(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check first activity structure
    chess_club = activities["Chess Club"]
    
    # Should have all required fields
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    # Verify types
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)


def test_get_activities_participants_are_emails(client):
    """Test that participants list contains email strings"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check that participants are valid email formats
    for activity_name, activity in activities.items():
        for participant in activity["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant
            assert ".edu" in participant
