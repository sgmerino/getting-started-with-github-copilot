"""
DELETE /activities/{activity_name}/participants endpoint tests using AAA (Arrange-Act-Assert) pattern.
Tests participant removal, error cases, and edge cases.
"""


def test_delete_participant_success(client):
    """Test that an existing participant can be successfully removed from an activity."""
    # Arrange: Participant exists in activity
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    
    # Act: Remove participant
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email_to_remove}
    )
    
    # Assert: Verify success
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email_to_remove} from {activity_name}"
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email_to_remove not in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 1


def test_delete_nonexistent_activity_returns_404(client):
    """Test that deleting from non-existent activity returns 404."""
    # Arrange: Activity doesn't exist
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act: Try to remove from non-existent activity
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_nonexistent_participant_returns_404(client):
    """Test that deleting non-existent participant returns 404."""
    # Arrange: Participant not in activity
    activity_name = "Chess Club"
    email = "notamember@mergington.edu"
    
    # Act: Try to remove non-existent participant
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_delete_all_participants_from_activity(client):
    """Test that all participants can be removed from an activity one by one."""
    # Arrange: Activity has participants
    activity_name = "Chess Club"
    participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act: Remove all participants
    for email in participants:
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert: Activity should have no participants
    activities = client.get("/activities").json()
    assert len(activities["Chess Club"]["participants"]) == 0
