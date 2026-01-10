from imap_client import IMAPClient
from classifier import Classifier
from router import Router
import config
import time

TIMEOUT = 30

def main():
    imap_client = IMAPClient(config.IMAP_HOST, config.IMAP_USER, config.IMAP_PASS)
    classifier = Classifier()
    router = Router(imap_client)
    
    print(f"Email service started. Checking for new emails every {TIMEOUT} seconds.")

    try:
        print("Checking for new unseen emails...")
        messages = imap_client.fetch_unseen()
        if not messages:
            print("No new unseen emails found.")
        for uid, subject, sender, body in messages:
            label = classifier.classify(subject, body, sender)
            
            if label is None:
                print(f"Classification failed for email UID: {uid}. Skipping.")
                continue
            
            if label not in config.FOLDERS:
                continue
            
            router.route(uid, label)
    except Exception as e:
        print(f"An error occurred: {e}")
        

if __name__ == "__main__":
    main()