# Project Composer

Composer is a music generation application hosted on an iOS mobile device. The purpose of the app is to generate music from a provided input and generate harmonization for a given melody.

## The Idea

The aim of the project is to take the input of any music source and create something completely new. For example, Composer could sample an eight-second Musical Instrument Digital Interface (MIDI) file clip and come up with the rest, forming a new song right away. This new song would consist of harmonies that accompany the music piece as well.

## Generation Workflow Design

![Screenshot 2021-04-20 at 12 31 22 AM](https://user-images.githubusercontent.com/16576977/115271343-d01dfc80-a16f-11eb-876f-9e5e81eba580.png)

## Server Workflow Design

![Screenshot 2021-04-20 at 12 31 31 AM](https://user-images.githubusercontent.com/16576977/115271352-d14f2980-a16f-11eb-8873-98017807b581.png)


## iOS Mobile Workflow Design

![Screenshot 2021-04-20 at 12 31 41 AM](https://user-images.githubusercontent.com/16576977/115271411-e75cea00-a16f-11eb-8bbf-fed5fd4a4dc5.png)

## Deploying the backend on AWS

User should already have an account on AWS console, and have already created an AWS EC2 instance with the Deep Learning AMI (which has the necessary PyTorch libraries etc).

app.py, credentials.py should be in the same directory as the other python training scripts (e.g. lstm_train.py)

Dependencies required: gunicorn3, Flask

1) Start the EC2 instance from AWS console.

2) SSH into EC2 instance through Ubuntu (for example). More details can be found on the [AWS website](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html).

3) Update nginx configuration by first executing `cd /etc/nginx/sites-enabled` then copy the `flaskapp` file to the current working directory. Update server_name variable to the public IPv4 DNS of the EC2 instance (can be found on AWS console).

4) cd to application folder (where app.py is located)

5) Activate pytorch_p36 environment on the remote server by running `source activate pytorch_p36`

6) Update app.py and credentials.py with personal AWS services information.

7) Run the application with `sudo gunicorn3 app:app`. Can execute with set timeout option using `-t 120` if necessary.


## Future Plans (V2.0)

### iOS Mobile App
#### Expand song corpus
#### Add Piano Feature
### Build server-based backend
#### Port model training to cloud
### LSTM model Design
#### Improve sound quality
