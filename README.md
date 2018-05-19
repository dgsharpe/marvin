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

### Support Marvin Development
Donate via Bitcoin, 1KZGrTNjtthNEsf8fruWiMHiKD3zdm3hGY
