# Marvin (the paranoid file monitor)

Marvin monitors your files. When files or directories of your choosing are created, deleted, changed, moved, or renamed, Marvin logs it. Marvin can also send notifications about changes to files using email or [Pushover][po].

## Who is this for?

Marvin is for people who are paranoid about the integrity of their files. Your files can change without your knowledge due to mistakes, viruses, buggy applications, other users, and more. Backups and snapshots are great, but if you don't notice changes in time, your backups will be overwritten with the new (bad) file versions. With Marvin, you'll know about these changes in near-real time.

### Prerequisites

You need:

1) A Linux machine
2) Python 3.x and pip (on Ubuntu, `sudo apt install python3-pip`)
3) A free [Mailgun][mg] account and API key (if you want email notifications)
4) A free [Pushover][po] user and app token (if you want push notifications)

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
5) (optional) Set Marvin to run at system boot. Edit your crontab with `crontab -e` and add a line like this:
```
@reboot sleep 5; cd /path/to/marvin/; /usr/bin/screen -dm /usr/bin/python3 marvin.py
```

### Set up notifications (optional)

Notifications can be set up in the `marvin.config` file. Pushover can be used to send push notifications to iOS and Android devices. Mailgun can be used to send email notifications to a recipient. These can be used in any combination, or none at all.

#### Set up Mailgun for email notifications

You will need three pieces of information to configure Mailgun - an "Authorized Recipient" (the email address where you want the notifications to be sent), your Mailgun Private API Key, and your Mailgun domain. Here's how to get those.

1) Go to [mailgun.com][mg] and sign up for a free account. You do not need to enter your payment information, the free plan works just fine.
2) Click the activation link sent to your email to fully activate your account.
3) Click your email address at the top right, then go to Account Settings. Then click the "Authorized Recipients" tab.
4) Invite the email address you want notifications sent to. Mailgun will send a confirmation email to this address - click it to confirm the authorized recipient. Put this authorized recipient email address into your Marvin config as the "emailAddress"
5) Now click the "Security" tab, next to the Authorized Recipients tab. Click the eye icon to view your Private API Key. Put this into your Marvin config as the "apiKey"
6) Now click the "Domains" tab at the top of the page. You should now have one domain whose name starts with "sandbox". Copy its full name and put it into your Marvin config as the "domainName".
7) All set!

#### Set up Pushover for push notifications

You will need two pieces of information to set up Pushover notifications - your "User Key" and an "App Token". To get those:

1) Go to [pushover.net][po] and sign up for an account. All Pushover clients have a 7 day free trial, then have a one time cost of $4.99.
2) Once logged in, you should see your profile page, with your `User Key` in the upper right.
3) Under the section "Your Applications", select "Create an Application/API Token".
4) Name your application. Give it a description or image if desired. URL can be left blank.
5) Copy your new API token to your config, along with the user key.
6) Enjoy!

### Support Marvin Development
Donate via Bitcoin, 1KZGrTNjtthNEsf8fruWiMHiKD3zdm3hGY

[po]: https://pushover.net
[mg]: https://www.mailgun.com
