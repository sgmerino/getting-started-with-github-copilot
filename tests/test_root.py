"""
GET / endpoint tests using AAA (Arrange-Act-Assert) pattern.
Tests the root endpoint redirect to static/index.html.
"""


def test_root_redirects_to_static_index(client):
    """Test that GET / returns a redirect to /static/index.html."""
    # Arrange: root endpoint
    
    # Act: Make GET request to root
    response = client.get("/", follow_redirects=False)
    
    # Assert: Verify redirect
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_follows_redirect_to_index(client):
    """Test that following the redirect from / leads to /static/index.html."""
    # Arrange: root endpoint
    
    # Act: Make GET request with follow_redirects
    response = client.get("/", follow_redirects=True)
    
    # Assert: Should end at static/index.html
    assert response.status_code == 200
