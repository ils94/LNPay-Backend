from src.webhook import webhook_subscription

webhook_subscription.list_subscriptions()

id = input("Input the Webhook ID you want to change: ")

webhook_subscription.update_subscription(id)
