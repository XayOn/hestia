"""Main app."""

from .routes import setup_routes
from aiohttp import web

from cleo import Command
from cleo import Application

from gql import gql, Client, AIOHTTPTransport


async def setup_hasura(app):
    transport = AIOHTTPTransport(url=app['hasuraurl'],
                                 headers=dict(Authorization=app['hasurapw']))
    app['hasura'] = Client(transport=transport,
                           fetch_schema_from_transport=True)


class NotificationServerCommand(Command):
    """Starts server

    start_server
        {--host=0.0.0.0 : Host to listen on}
        {--port=8080 : Port to listen on}
        {--hasurapw=hasura : Hasura admin password}
        {--hasuraurl=http://hasura:8080/v1/graphql : Hasura url}
        {--debug : Debug and verbose mode}
    """
    def handle(self):
        """Handle command."""
        app = web.Application()
        app['hasuraurl'] = self.option('hasuraurl')
        app['hasurapw'] = self.option('hasurapw')
        app.on_startup.append(setup_hasura)
        setup_routes(app)
        web.run_app(app,
                    host=self.option('host'),
                    port=int(self.option('port')))


def main():
    """Main."""
    application = Application()
    application.add(NotificationServerCommand())
    application.run()
