# MIT License
#
# Copyright (c) 2025 ILS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import hashlib
import hmac


# Yes, it works.
def compute_hmac(content, secret):
    """Compute the HMAC SHA-256 for the given content and secret."""
    # I CAN'T FUCKING BELIVE THAT THIS SHIT HERE RETURNS THE THINGY IN LOWER CASE!
    # STRIKE SENDS THE SIGNATURE IN UPPER CASE!
    return hmac.new(secret.encode('utf-8'), content, hashlib.sha256).hexdigest().upper()


def verify_request_signature(raw_data, signature, secret):
    """Verify the request's signature."""
    computed_signature = compute_hmac(raw_data, secret)

    print(f"Computed HMAC: {computed_signature}")  # Debug line
    print(f"Provided Signature: {signature}")  # Debug line

    return hmac.compare_digest(computed_signature, signature)
