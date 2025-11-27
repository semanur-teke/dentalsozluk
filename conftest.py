"""
Pytest configuration and fixtures for dentalsozluk project.
"""
import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory


@pytest.fixture
def request_factory():
    """Pytest fixture for Django RequestFactory."""
    return RequestFactory()


@pytest.fixture
def mock_request(request_factory):
    """Create a mock Django request with session support."""
    request = request_factory.get('/')

    # Add session support
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

    return request


@pytest.fixture
def dental_term(db):
    """Create a sample DentalTerm for testing."""
    from terms.models import DentalTerm
    return DentalTerm.objects.create(
        title="Test Terim",
        description="Test açıklaması",
        english_equivalent="Test Term",
        latin_equivalent="Testus terminus",
        slug="test-terim"
    )


@pytest.fixture
def multiple_terms(db):
    """Create multiple DentalTerms for testing."""
    from terms.models import DentalTerm
    terms = [
        DentalTerm.objects.create(
            title=f"Terim {i}",
            description=f"Açıklama {i}",
            slug=f"terim-{i}"
        )
        for i in range(1, 6)
    ]
    return terms
