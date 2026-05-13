"""
POST /activities/{activity_name}/signup endpoint tests using AAA (Arrange-Act-Assert) pattern.
Tests signup functionality, duplicate prevention, and error cases.
"""


def test_signup_success_adds_participant(client):
    """Test that a new participant can successfully sign up for an activity."""
    # Arrange: Start with clean activities
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act: Sign up new participant
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert: Verify success and participant added
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    
    # Verify participant was added
    activities_response = client.get("/activities")
    updated_activity = activities_response.json()["Chess Club"]
    assert new_email in updated_activity["participants"]
    assert len(updated_activity["participants"]) == 3


def test_signup_duplicate_returns_400(client):
    """Test that duplicate signup is prevented with 400 error."""
    # Arrange: Existing participant
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    
    # Act: Try to sign up already-registered participant
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert: Verify error response
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signup to non-existent activity returns 404."""
    # Arrange: Activity that doesn't exist
    activity_name = "Nonexistent Club"
    new_email = "student@mergington.edu"
    
    # Act: Try to sign up for non-existent activity
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_multiple_different_activities(client):
    """Test that same participant can sign up for multiple activities."""
    # Arrange: Same participant, different activities
    email = "newstudent@mergington.edu"
    
    # Act: Sign up for first activity
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    # Act: Sign up for second activity
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    
    # Assert: Both signups should succeed
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify participant is in both activities
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]
