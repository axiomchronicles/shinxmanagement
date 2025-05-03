from aquilify.core.schematic.routing import rule
from . import (
    register,
    otp_resend,
    otp_verification,
    document_upload
)

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
    rule("/register", register.shinxManagementRegistrationServerMethod.openAccountFormRoute, methods = ['POST']),
    rule("/verify", otp_verification.authenticationotpverification.main, methods = ['POST']),
    rule("/resend", otp_resend.authenticationresend.main, methods = ['POST']),
    rule("/identity", document_upload.documentverification.main, methods = ['POST']),
]
