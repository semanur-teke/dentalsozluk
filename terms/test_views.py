"""
Integration tests for terms views.
"""
import pytest
import json
from django.urls import reverse
from django.test import Client
from terms.models import DentalTerm, ErrorReport


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.mark.django_db
class TestHomeView:
    """Test cases for home view."""

    def test_home_page_loads(self, client):
        """Test that home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert 'hide_search' in response.context


@pytest.mark.django_db
class TestTermDetailView:
    """Test cases for term detail view."""

    def test_term_detail_loads(self, client, dental_term):
        """Test that term detail page loads successfully."""
        url = reverse('terms:term_detail', kwargs={'slug': dental_term.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['term'] == dental_term

    def test_term_detail_404(self, client):
        """Test that non-existent term returns 404."""
        url = reverse('terms:term_detail', kwargs={'slug': 'nonexistent'})
        response = client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestSearchView:
    """Test cases for search functionality."""

    def test_search_with_query(self, client, dental_term):
        """Test search with valid query."""
        response = client.get('/search/', {'q': dental_term.title})
        assert response.status_code == 200
        assert response.context['matched_term'] == dental_term

    def test_search_no_results(self, client):
        """Test search with no results."""
        response = client.get('/search/', {'q': 'nonexistent term'})
        assert response.status_code == 200
        assert response.context['matched_term'] is None


@pytest.mark.django_db
class TestReportErrorView:
    """Test cases for error reporting endpoint."""

    def test_report_error_success(self, client, dental_term):
        """Test successful error report submission."""
        # Enable session
        session = client.session
        session.save()

        response = client.post(
            '/report_error/',
            data={
                'term_id': dental_term.id,
                'honeypot': ''
            }
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['status'] == 'success'

        # Verify error report was created
        assert ErrorReport.objects.filter(term=dental_term).exists()

    def test_report_error_duplicate(self, client, dental_term):
        """Test duplicate error report within timeframe."""
        session = client.session
        session.save()

        # First report
        client.post('/report_error/', {
            'term_id': dental_term.id,
            'honeypot': ''
        })

        # Second report (should be rejected)
        response = client.post('/report_error/', {
            'term_id': dental_term.id,
            'honeypot': ''
        })

        data = json.loads(response.content)
        assert data['status'] == 'info'
        assert 'bildirildi' in data['message'].lower()

    def test_report_error_bot_detection(self, client, dental_term):
        """Test bot detection via honeypot."""
        response = client.post('/report_error/', {
            'term_id': dental_term.id,
            'honeypot': 'bot_value'
        })

        assert response.status_code == 400
        data = json.loads(response.content)
        assert data['status'] == 'error'

    def test_report_error_missing_term_id(self, client):
        """Test error report without term_id."""
        response = client.post('/report_error/', {
            'honeypot': ''
        })

        assert response.status_code == 400
        data = json.loads(response.content)
        assert data['status'] == 'error'

    def test_report_error_invalid_term_id(self, client):
        """Test error report with non-existent term_id."""
        response = client.post('/report_error/', {
            'term_id': 99999,
            'honeypot': ''
        })

        assert response.status_code == 404


@pytest.mark.django_db
class TestAutocomplete:
    """Test cases for autocomplete functionality."""

    def test_autocomplete_with_results(self, client, multiple_terms):
        """Test autocomplete returns matching results."""
        response = client.get('/autocomplete/', {'q': 'Terim'})
        assert response.status_code == 200

        data = json.loads(response.content)
        assert len(data) > 0
        assert all('title' in item and 'url' in item for item in data)

    def test_autocomplete_short_query(self, client):
        """Test autocomplete rejects queries shorter than 2 chars."""
        response = client.get('/autocomplete/', {'q': 'a'})
        assert response.status_code == 200

        data = json.loads(response.content)
        assert len(data) == 0

    def test_autocomplete_no_query(self, client):
        """Test autocomplete with empty query."""
        response = client.get('/autocomplete/')
        assert response.status_code == 200

        data = json.loads(response.content)
        assert len(data) == 0
