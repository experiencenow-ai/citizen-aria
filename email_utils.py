"""
Local Email Utilities for Aria
Email: aria@opustrace.com (local mail via Maildir)
"""
import subprocess
import mailbox
import email
from email.header import decode_header
import os
from datetime import datetime

# Use Maildir format (where postfix actually delivers)
MAILDIR_PATH = "/home/aria/Maildir"
FROM_ADDRESS = "aria@opustrace.com"

def send_email(to: str, subject: str, body: str) -> bool:
    """Send email using local sendmail."""
    try:
        msg = f"""From: {FROM_ADDRESS}
To: {to}
Subject: {subject}
Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}
Content-Type: text/plain; charset=utf-8

{body}
"""
        proc = subprocess.run(
            ['/usr/sbin/sendmail', '-t'],
            input=msg.encode('utf-8'),
            capture_output=True,
            timeout=30
        )
        return proc.returncode == 0
    except Exception as e:
        print(f"Email send error: {e}")
        return False

def check_email(max_results: int = 10, unread_only: bool = False) -> list:
    """Check Maildir for messages."""
    results = []
    try:
        if not os.path.exists(MAILDIR_PATH):
            return []
        
        mdir = mailbox.Maildir(MAILDIR_PATH)
        
        # Get all messages from new and cur
        messages = []
        for key, msg in mdir.items():
            messages.append((key, msg))
        
        # Sort by date (most recent last) and limit
        messages = messages[-max_results:] if len(messages) > max_results else messages
        
        for key, msg in messages:
            subject = msg.get('Subject', '(no subject)')
            if subject:
                decoded = decode_header(subject)
                subject = ''.join(
                    part.decode(enc or 'utf-8') if isinstance(part, bytes) else str(part)
                    for part, enc in decoded
                )
            
            from_addr = msg.get('From', 'unknown')
            date = msg.get('Date', '')
            
            # Get body preview
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='replace')
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='replace')
            
            results.append({
                "id": str(key),
                "from": from_addr,
                "subject": subject,
                "date": date,
                "body_preview": body[:500] + "..." if len(body) > 500 else body
            })
        
        mdir.close()
    except Exception as e:
        print(f"Email check error: {e}")
    
    return results

def get_email_by_id(email_id: str) -> dict:
    """Get full email by Maildir key."""
    try:
        if not os.path.exists(MAILDIR_PATH):
            return None
        
        mdir = mailbox.Maildir(MAILDIR_PATH)
        
        if email_id in mdir:
            msg = mdir[email_id]
            
            subject = msg.get('Subject', '(no subject)')
            if subject:
                decoded = decode_header(subject)
                subject = ''.join(
                    part.decode(enc or 'utf-8') if isinstance(part, bytes) else str(part)
                    for part, enc in decoded
                )
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='replace')
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='replace')
            
            mdir.close()
            return {
                "id": email_id,
                "from": msg.get('From', 'unknown'),
                "to": msg.get('To', ''),
                "subject": subject,
                "date": msg.get('Date', ''),
                "body": body
            }
        
        mdir.close()
        return None
    except Exception as e:
        print(f"Email get error: {e}")
        return None

def mark_as_read(email_id: str) -> bool:
    """Mark email as read (move from new to cur with :2,S flag)."""
    try:
        mdir = mailbox.Maildir(MAILDIR_PATH)
        if email_id in mdir:
            msg = mdir[email_id]
            msg.add_flag('S')  # Seen flag
            mdir[email_id] = msg
            mdir.close()
            return True
        mdir.close()
        return False
    except Exception as e:
        print(f"Mark read error: {e}")
        return False
