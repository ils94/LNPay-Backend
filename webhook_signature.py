import hmac
import hashlib
import global_variables


def verify(data, signature):
    """
    Verifies the HMAC SHA256 signature of the incoming webhook request.
    """
    computed_signature = hmac.new(
        global_variables.webhook_secret.encode(),
        data,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)
