"""
GET /activities endpoint tests using AAA (Arrange-Act-Assert) pattern.
Tests the endpoint that returns all available activities.
"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities from sample data."""
    # Arrange: activities fixture already set up with clean data
    
    # Act: Make GET request
    response = client.get("/activities")
    
    # Assert: Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_returns_correct_structure(client):
    """Test that activity objects contain all required fields."""
    # Arrange: activities fixture already set up
    
    # Act: Make GET request
    response = client.get("/activities")
    data = response.json()
    
    # Assert: Verify activity structure
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_shows_participant_counts(client):
    """Test that activities show correct participant information."""
    # Arrange: activities fixture already set up
    
    # Act: Make GET request
    response = client.get("/activities")
    data = response.json()
    
    # Assert: Verify participant data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
    assert len(data["Programming Class"]["participants"]) == 2
    assert data["Gym Class"]["max_participants"] == 30
