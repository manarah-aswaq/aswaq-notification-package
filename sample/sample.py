from aswaq_notifications import NotificationClient

client = NotificationClient("0828a6e1cd8b6a5cb1e422070713c71226fd5e3c")
notification = client.send_notifications(
    message_data='{"url": "","body": {"action": "product","type": 2,"value": {"type": "product","value": "3113"}},"message": "hi"}',
    user_tokens=[
        "eC9tL3yNf08:APA91bHf86EsUNaWeIDBC-4ki_MC95iGWWJRVhfIaWs4d_W6Kn4eWALTqvBhPOpDDbtowZgWMs3UWUUVmjkHqRRkYtgKdM4Z-3DFKDm7bPjTA-viHT8aMdoonjlLBGh1XBDPy0mpIf2K"]
)
print(notification)