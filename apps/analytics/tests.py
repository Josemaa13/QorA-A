from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.urls import reverse

User = get_user_model()

class AnalyticsMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    @patch('analytics.services.services.mongodb_client.insert_one')
    def test_middleware_tracks_page_view(self, mock_insert):
        # We need a valid view to test it. Let's just mock a simple get to the home page.
        # Assuming '/' returns 200 OK.
        self.client.get('/')
        self.assertTrue(mock_insert.called)
        
        args, kwargs = mock_insert.call_args
        self.assertEqual(args[0], 'analytics')
        self.assertEqual(args[1]['event_type'], 'page_view')
        self.assertEqual(args[1]['url_path'], '/')

class AnalyticsDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='password123')
        self.regular_user = User.objects.create_user(username='regular', password='password123')

    @patch('analytics.views.get_recent_page_views', return_value=[])
    @patch('analytics.views.get_recent_searches', return_value=[])
    def test_dashboard_access_for_admin(self, mock_searches, mock_page_views):
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('analytics:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_access_denied_for_regular_user(self):
        self.client.login(username='regular', password='password123')
        response = self.client.get(reverse('analytics:dashboard'))
        # Should redirect because user_passes_test restricts it
        self.assertEqual(response.status_code, 302)
