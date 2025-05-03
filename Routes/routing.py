from aquilify.core.schematic.routing import rule
from .authentication import (
    register,
    otp_verification,
    document_upload,
    account_timeline,
    thankyou_msg
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
    # API's Routing..........
    rule("/account/register", register.accountAuthenticationViewRoute ,methods = ['GET'], name = "Authentication Registration Route's"),
    rule("/account/document", document_upload.documentUploadViewRoute ,methods = ['GET'], name = "Authentication Document Upload Route's"),
    rule("/account/thankyou", thankyou_msg.thankyouMsgViewRoute ,methods = ['GET'], name = "Authentication Thnakyou Message Route's"),
    rule("/account/verify", otp_verification.accountVerificationViewRoute ,methods = ['GET'], name = "Authentication Verification Route's"),
    rule("/account/timeline", account_timeline.accountTimelineViewRoute ,methods = ['GET'], name = "Authentication Account Timeline Route's"),
]
