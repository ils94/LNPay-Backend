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

import datetime


# correlation_id needs to be unique, otherwise it will return an error from Strike API. Using the current local
# machine time was the easiest approach I came up with. Both description and correlation_id can be used as identifiers
# for your project, but remember that correlation_id MUST BE DIFFERENT FROM ALL OTHERS EVERYTIME

def generate_correlation_id():
    now = datetime.datetime.now()

    correlation_id = now.strftime('%d%m%Y%H%M%S') + f'{now.microsecond // 10000}{(now.microsecond % 10000) // 100}'

    return correlation_id


def generate_description():
    description = ""

    # Your logic to generate a description for your invoices here

    return description
