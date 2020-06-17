# Automating AWS with Python

Repository for the ACG course *Automating AWS with Python*

## 01-webotron

Webotron is a script that will sync a local directory to an S3 bucket and optionally configure Route 53 and CloudFront aswell.

### Features

Webotron currently has the following features:

- List bucket
- List contents of a bucket
- Create and set up bucket
- Sync directory tree to bucket
- Set AWS profile with --profile=<profileName>
- Sets up a hosted zone / A record for Route 53
- Sets up a CDN

## 02-notifon

Notifon is a project to notify Slack users of changes to your AWS account using CloudWatch Events

### Features

Notifon currently has the following features:

- Post CloudWatch Auto Scaling events to a Slack webhook
