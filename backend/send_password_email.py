#!/usr/bin/env python3
"""
Send password reset email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_password_email(to_email, username, new_password):
    """Send the new password to the user via email"""

    # Email configuration - using Gmail
    from_email = "your-email@gmail.com"  # Replace with your Gmail
    from_name = "Family Tree Admin"

    # You'll need to use an App Password from your Google Account
    # NOT your regular password
    smtp_password = os.getenv('GMAIL_APP_PASSWORD')

    if not smtp_password:
        print("ERROR: Please set GMAIL_APP_PASSWORD environment variable")
        print("To create an app password:")
        print("1. Go to your Google Account")
        print("2. Select Security > 2-Step Verification")
        print("3. At the bottom, select App passwords")
        print("4. Create a new app password for 'Mail'")
        print("5. Set it: set GMAIL_APP_PASSWORD=your-16-char-password")
        return False

    subject = "Your New Login Credentials - Family Tree Website"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background: #ffffff;
                padding: 30px;
                border: 1px solid #e0e0e0;
                border-top: none;
            }}
            .credentials {{
                background: #f8f9fa;
                border: 2px solid #667eea;
                padding: 20px;
                margin: 25px 0;
                border-radius: 8px;
            }}
            .cred-item {{
                margin: 10px 0;
            }}
            .cred-label {{
                font-weight: bold;
                color: #666;
            }}
            .cred-value {{
                font-family: 'Courier New', monospace;
                font-size: 18px;
                color: #667eea;
                background: white;
                padding: 8px 12px;
                border-radius: 4px;
                display: inline-block;
                margin-top: 5px;
            }}
            .button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-radius: 0 0 8px 8px;
                font-size: 14px;
                color: #666;
            }}
            .warning {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Your New Login Credentials</h1>
        </div>

        <div class="content">
            <p>Hi {username},</p>

            <p>Your password has been reset as requested. Here are your new login credentials:</p>

            <div class="credentials">
                <div class="cred-item">
                    <div class="cred-label">Username:</div>
                    <div class="cred-value">{username}</div>
                </div>
                <div class="cred-item">
                    <div class="cred-label">New Password:</div>
                    <div class="cred-value">{new_password}</div>
                </div>
            </div>

            <div class="warning">
                <strong>Important:</strong> For security, please change this password after logging in.
                You can do this in your account settings.
            </div>

            <div style="text-align: center;">
                <a href="http://localhost:3000/login" class="button">Go to Login Page</a>
            </div>

            <p style="margin-top: 30px;">If you did not request this password reset, please contact the administrator immediately.</p>
        </div>

        <div class="footer">
            <p>This is an automated email from the Family Tree website.</p>
            <p>Please do not reply to this email.</p>
        </div>
    </body>
    </html>
    """

    text_body = f"""
    Hi {username},

    Your password has been reset. Here are your new login credentials:

    Username: {username}
    New Password: {new_password}

    Login at: http://localhost:3000/login

    IMPORTANT: For security, please change this password after logging in.

    If you did not request this reset, please contact the administrator immediately.

    ---
    This is an automated email from the Family Tree website.
    """

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = to_email

        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        print(f"Connecting to Gmail SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, smtp_password)
            server.send_message(msg)

        print(f"Successfully sent password to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    # Send the password
    send_password_email("bgladney02@gmail.com", "ben", "kVBDvPGjmedN")
