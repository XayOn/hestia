"""Routes."""
from .handlers import week_menu


def setup_routes(app):
    """Setup routes."""
    app.router.add_post('/weekMenu', week_menu.index)
