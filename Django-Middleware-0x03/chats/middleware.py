import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

# --------------------------
# 1. Logging User Requests
# --------------------------
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        response = self.get_response(request)
        return response

# --------------------------
# 2. Restrict Chat Access by Time
# --------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Deny access if outside 6AM to 9PM
        if now < time(6, 0) or now > time(21, 0):
            return HttpResponseForbidden("Chat access is allowed only between 6AM and 9PM")
        return self.get_response(request)

# --------------------------
# 3. Limit Chat Messages per IP
# --------------------------
class OffensiveLanguageMiddleware:
    """
    Middleware that limits number of POST requests per IP.
    Example: max 5 messages per minute.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()
            # Keep only timestamps within last 60 seconds
            self.ip_requests[ip] = [ts for ts in self.ip_requests[ip] if now - ts < timedelta(minutes=1)]
            if len(self.ip_requests[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")
            self.ip_requests[ip].append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# --------------------------
# 4. Enforce Role Permissions
# --------------------------
class RolePermissionMiddleware:
    """
    Allow only users with 'admin' or 'moderator' role for certain actions.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: Only restrict POST, PUT, DELETE for messages/conversations
        restricted_paths = ['/api/messages/', '/api/conversations/']
        if any(request.path.startswith(p) for p in restricted_paths) and request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if not request.user.is_authenticated or getattr(request.user, 'role', '').lower() not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)
