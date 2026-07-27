# Marvin (the paranoid file monitor)

Marvin monitors your files. When files or directories are created, deleted, changed, moved, or renamed, Marvin logs it. Marvin can also send notifications using email or [Pushover][po].

## Who is this for?

Marvin is for people who never want to lose valuable data. Your files can change without your knowledge due to mistakes, viruses, buggy applications, other users' actions, and more. Backups and snapshots are great, but they only help if you notice that your files were changed *before* it's too late. If you don't, your backups will eventually be overwritten with the changed file versions. Marvin solves the problem by logging changes and notifying you about them in near real-time.

## Prerequisites

You need:

1) A Linux machine
2) Python 3.11 or newer, and the venv module (on Ubuntu-like distros, `sudo apt install python3-venv`)
3) (optional) An email account from which to send notifications, if you want to send yourself email notifications
4) (optional) A free [Mailgun][mg] account and API key, if you want to send email notifications through Mailgun
5) (optional) A free [Pushover][po] user and app token, if you want push notifications via Pushover

## Configuration

1) Download this repository
   ```
   sudo git clone https://github.com/dgsharpe/marvin.git /opt/marvin
   ```
2) Rename example-config.json to config.json and edit it to your preferences. It can hold API keys and passwords, so restrict it with `sudo chmod 600 /opt/marvin/config.json`
3) Install the required libraries into a virtual environment:
   ```
   sudo python3 -m venv /opt/marvin/.venv
   sudo /opt/marvin/.venv/bin/pip install -r /opt/marvin/requirements.txt
   ```
4) If your distribution uses systemd (as Ubuntu and most other popular distributions do), then do the following to run Marvin as a background service: 

Create a file at `/etc/systemd/system/marvin.service` like this, changing the values as appropriate:
```
    [Install]
    WantedBy=multi-user.target
    
    [Unit]
    Description=Marvin - The Paranoid File Monitor
    After=local-fs.target
    
    [Service]
    Type=simple
    User=root
    Group=root
    WorkingDirectory=/opt/marvin/
    ExecStart=/opt/marvin/.venv/bin/python /opt/marvin/marvin.py
    Restart=always
    RestartSec=5
```
Then run `sudo systemctl daemon-reload && sudo systemctl enable marvin.service && sudo systemctl start marvin.service`

If Marvin detects that one of its own threads has died, it logs the reason and exits so that systemd restarts it. Should the underlying fault be permanent (ex. a watch path that never exists) systemd gives up after a few attempts and marks the unit `failed`, so check `systemctl status marvin.service` if notifications stop arriving.

5) If your distribution does not use systemd, you can run Marvin in the background with the 'screen' utility, as in, `screen /opt/marvin/.venv/bin/python marvin.py`. Furthermore, you can set Marvin to run via screen at system boot, using cron. Edit your crontab with `crontab -e` and add a line like this (changing the paths to Marvin and screen as needed): `@reboot sleep 5; cd /opt/marvin/; /usr/bin/screen -dm /opt/marvin/.venv/bin/python marvin.py`

6) If you are watching a large directory tree with `recursion` enabled, Marvin needs one kernel watch per directory. The default limit is low (8192 on smaller machines), and exceeding it stops Marvin from watching further directories. Check yours with `cat /proc/sys/fs/inotify/max_user_watches`, and raise it if needed by adding `fs.inotify.max_user_watches=524288` to `/etc/sysctl.conf` and running `sudo sysctl -p`

## Set up notifications (optional)

Notifications can be configured in the `config.json` file. You can have Marvin email you directly, you can send emails via Mailgun, and you can use Pushover to send push notifications to iOS and Android devices. These can be used in any combination, or skipped entirely.

#### Set up email notifications locally (recommended)

This section will guide you through setting up your computer for sending emails from an email account of your choice. These instructions are tested on Debian and Ubuntu, but will be similar for other distributions. Marvin sends local mail by piping to the `mail` command, which needs both a mail user agent and a mail transfer agent (MTA). You might need to install one or both.

**If you are running Proxmox VE, do not install ssmtp or msmtp-mta.** Proxmox already installs Postfix and sends its own notifications through it. Every MTA package declares `Conflicts: mail-transport-agent`, so installing a second one removes Postfix and breaks Proxmox notifications. Skip to step 4 — Postfix already satisfies everything Marvin needs.

**If you're sending from a Gmail account**, Gmail requires an [app-specific password][gmail-asp], which in turn requires 2-Step Verification to be enabled on the account.

1) If you already have an MTA such as Postfix or Exim configured, skip to step 4.
2) Install msmtp as a relay-only MTA with `sudo apt install msmtp msmtp-mta`.
3) Edit the config file: `sudo nano /etc/msmtprc`, then restrict it with `sudo chmod 600 /etc/msmtprc`. Copy-paste the following, but **replace the values with parameters from your email provider and account**. The example values here are from Gmail:
   ```
   defaults
   auth           on
   tls            on
   tls_trust_file /etc/ssl/certs/ca-certificates.crt
   logfile        /var/log/msmtp.log

   account        default
   host           smtp.gmail.com
   port           587
   from           disposable-email-account@gmail.com
   user           disposable-email-account@gmail.com
   password       disposable-email-account-app-password
   ```
4) Install the `mail` command with `sudo apt install bsd-mailx`
5) Run a test to make sure everything is working: 
    ```
    echo "hello world" | mail -s "Test Email" your-recipient-email-address@somewebsite.com
    ```
6) In your Marvin `config.json` file, enable the localMail notifier, and set the recipient email address.

#### Set up Mailgun for email notifications

Before setting up free emails via a Mailgun "sandbox" domain, be aware that Mailgun does not intend users to use sandboxes forever. If you do not have a real domain associated with your Mailgun account, you may have your free sandbox stop working eventually. Marvin will work the same with a fully-configured domain as with a free sandbox domain, so if you already have a configured domain, feel free to simply enter your API Key and Domain Name into the `config.json` file. If you don't but want to try Mailgun, read on.


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
[gmail-asp]: https://support.google.com/accounts/answer/185833?hl=en
