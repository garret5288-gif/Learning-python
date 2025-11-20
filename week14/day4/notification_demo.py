from notification import NotificationManager, EmailNotifier, SMSNotifier, NotificationError


def main():
    email = EmailNotifier(sender_alias="noreply@example.com", fail_first_n=1)
    sms = SMSNotifier(sender_alias="ExampleCo")
    manager = NotificationManager(email_notifier=email, sms_notifier=sms, retries=2)

    print("-- Email with retry --")
    manager.send_email("user@example.com", subject="Welcome", body="Thanks for joining!")

    print("-- SMS segmented --")
    long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
    manager.send_sms("+15551234567", body=long_text)

    print("-- Template helpers --")
    manager.send_email_template(
        "user@example.com",
        subject_tmpl="Hello {name}",
        body_tmpl="Your order #{order_id} total is ${amount}",
        context={"name": "Alex", "order_id": 42, "amount": 19.99},
    )

    print("-- Fallback: try email, then SMS --")
    try:
        # Force email to fail by setting fail_first_n higher than retries
        failing_email = EmailNotifier(sender_alias="noreply@example.com", fail_first_n=5)
        fallback_mgr = NotificationManager(email_notifier=failing_email, sms_notifier=sms, retries=1)
        channel = fallback_mgr.notify_with_fallback(
            to_email="user@example.com",
            to_phone="+15550001111",
            subject="Alert",
            body="Email unreachable, sending SMS...",
        )
        print(f"Delivered via: {channel}")
    except NotificationError as e:
        print("Both channels failed:", e)

if __name__ == "__main__":
    main()
