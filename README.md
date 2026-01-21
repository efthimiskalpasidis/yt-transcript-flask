# YouTube Transcript

A small personal project where I built and deployed a Flask application that fetches YouTube transcripts and caches them in a MySQL database.
The main goal was not the app itself, but instead to learn how to containerize an app, deploy it on Azure VM, and understand the full flow from local development to running service on Azure.

---

## Technologies
- Python (Flask)
- MySQL
- Docker and Docker Compose
- Azure VM (Ubuntu)
- yt-dlp

---

## Features

- Accepts a YouTube URL
- Fetches the transcript using 'yt-dlp'
- Stores the transcript in a MySQL db
- Returns cached transcripts if the same video is requested again
- Frontend to test the functionality

---

## Deployment process

Deployed manually on Azure VM:
1. Created a Linux VM in Azure (Ubuntu)
2. Connected to the VM using SSH
3. Installed Docker and Docker Compose
4. Cloned the GitHub repo on the VM
5. Built and started the application using 'docker compose'
6. Opened inbound port 80 in Azure to expose the app publicly

---

## CI/CD (Jenkins)

After the manual deployment, Jenkins was added to automate deployments.

- Jenkins runs on the same Azure VM
- A Jenkins pipeline is defined using Jenkinsfile
- Each push to main branch triggers:
  - git pull
  - docker compose down
  - docker compose up --build
- GitHub webhooks are used to trigger the pipeline automatically

## What I learned

- How Docker images are built using Dockerfile
- How Docker Compose connects services and networks
- How to troubleshoot container and networking issues
- How to work with SSH keys and remote servers
- How Azure networking (NSG / inbound rules) affects accessibility

---

## Notes and limitations

- Currently every push to the main branch triggers, including changes like readme. 
- On a small VM (1GB RAM) , swap was required to run MySQL, Docker and Jenkins together.
