from aquilify.core.routing import rule, include

# ROUTER configuration.

# The `ROUTER` list routes URLs to views.
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to ROUTER:  rule('/', views.home, name='home')
# Including another ROUTING
#     1. Import the include() function: from aquilify.core.routing import include, rule
#     2. Add a URL to ROUTER:  rule('/blog', include = include('blog.routing'))

ROUTER = [
    # API's Routing..........
    rule("/api/authentication", include = include("authentication.routing"), methods = ['GET', 'POST'], name = "Authentication API Route's"),
    rule("/shinxmanagement", include = include("Routes.routing"), methods = ['GET', 'POST'], name = "Authentication API Route's"),
]
