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

from src.webhook import webhook_subscription
import sys


def clear_terminal():
    """Simulate clearing the terminal by printing new lines."""
    print("\n" * 100)  # Prints 100 newlines to simulate clearing the terminal


def terminal_menu():
    while True:
        clear_terminal()
        print("\n--- Webhook Management Menu ---\n")
        print("1. Subscribe to a webhook")
        print("2. Unsubscribe from a webhook")
        print("3. Update a Subscription")
        print("4. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                clear_terminal()
                print("\n--- Webhook Subscription List ---\n")
                webhook_subscription.list_subscriptions()
                print("\n--- Subscribe to a Webhook ---\n")
                back = input("Enter 'b' to go back or press Enter to continue: ")
                if back.lower() == 'b':
                    break
                webhook_subscription.subscribe()

        elif choice == "2":
            while True:
                clear_terminal()
                print("\n--- Webhook Subscription List ---\n")
                webhook_subscription.list_subscriptions()
                print("\n--- Unsubscribe from a Webhook ---\n")
                x = input("Enter 'b' to go back or enter the Subscription ID to unsubscribe: ")
                if x.lower() == 'b':
                    break
                else:
                    webhook_subscription.unsubscribe(x)

        elif choice == "3":
            while True:
                clear_terminal()
                print("\n--- Webhook Subscription List ---\n")
                webhook_subscription.list_subscriptions()
                print("\n--- Update a Subscription ---\n")
                x = input("Enter 'b' to go back or enter the Subscription ID to update: ")
                if x.lower() == 'b':
                    break
                else:
                    webhook_subscription.update_subscription(x)

        elif choice == "4":
            clear_terminal()
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    terminal_menu()
