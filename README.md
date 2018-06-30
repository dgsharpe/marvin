# Marvin (the paranoid file monitor)

Marvin monitors your files. When files or directories of your choosing are created, deleted, changed, moved, or renamed, Marvin logs it. Marvin can also email you about the changes it detects.

## Who is this for?

Marvin is for people who are paranoid about the integrity of their files. Your files can change without your knowledge due to mistakes, viruses, buggy applications, other users, and more. Backups and snapshots are great, but if you don't notice changes in time, your backups will be overwritten with the new (bad) file versions. With Marvin, you'll know about these changes in near-real time.

### Prerequisites

You need:

1) A Linux machine
2) Python 3.x and pip (on Ubuntu, `sudo apt install python3-pip`)
3) A free Mailgun account and API key (if you want email notifications)

### Configuration

1) Download this repository
```
git clone https://github.com/davidgsharpe7/marvin.git
```
2) Rename example-config.json to config.json and edit it to your preferences.
3) Install the required libraries with pip. On Ubuntu, `sudo python3 -m pip install -r requirements.txt`
4) Run the application and leave it running. I prefer to run it with 'screen', as in:
```
screen python3 marvin.py
```

### Set up Mailgun for email notifications (optional)

You will need three pieces of information to configure Mailgun - an "Authorized Recipient" (the email address where you want the notifications to be sent), your Mailgun Private API Key, and your Mailgun domain. Here's how to get those.

1) Go to mailgun.com and sign up for a free account. You do not need to enter your payment information, the free plan works just fine. 
2) Click the activation link sent to your email to fully activate your account. 
3) Click your email address at the top right, then go to Account Settings. Then click the "Authorized Recipients" tab. 
4) Invite the email address you want notifications sent to. Mailgun will send a confirmation email to this address - click it to confirm the authorized recipient. Put this authorized recipient email address into your Marvin config as the "emailAddress" 
5) Now click the "Security" tab, next to the Authorized Recipients tab. Click the eye icon to view your Private API Key. Put this into your Marvin config as the "apiKey" 
6) Now click the "Domains" tab at the top of the page. You should now have one domain whose name starts with "sandbox". Copy its full name and put it into your Marvin config as the "domainName".
7) All set!

### Support Marvin Development
Donate via Bitcoin, 1KZGrTNjtthNEsf8fruWiMHiKD3zdm3hGY
