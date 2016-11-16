### How to deploy a new DSD instance?

#### Set up the AWS EC2 instance.
   t2.medium is the recommended EC2 type when deploying a new DSD instance. Please refer to the following server specs:
   - OS: Ubuntu 14.04.2 LTS (trusty)
   - CPU: 2vCPU
   - RAM: 4GB
   - Storage: 64GB

#### Create the settings file on EC2 instance
Since the dsd project is open source project and source code is hosted on Github. So any sensitive information is not in codebase.

For deployment, you need to first create a folder */opt/app/chai/volume/config*, then place *settings.ini* into this folder.

Please ask devs for *settings.ini* or copy from the existing prod server.

#### Get the certificate from *Let's encrypt it*
1. Log in the instance and install **certbot**
``` bash
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
```
2. Make sure TCP ports 80 and 443 on the instance is open.
3. Get the certificates.
``` bash
./certbot-auto certonly --standalone -d portalmbes.com -d portalmbes.com
```
4. Create a folder to store the linked certificates
``` bash
sudo mkdir -p /opt/app/chai/volume/config/ssl
```
5. Link the cert and private key
``` bash 
sudo ln -sf /etc/letsencrypt/live/portalmbes.com/fullchain.pem /opt/app/chai/volume/config/ssl/fullchain.pem
sudo ln -sf /etc/letsencrypt/live/portalmbes.com/privkey.pem /opt/app/chai/volume/config/ssl/privkey.pem
```

#### Create cronjob to update certificates automatically
Since the certificate got from *let's encrypt it* only can lasts for 90 days, so we need a cronjob to update the certificate automatically.   
1. Create a script named 'update-cert.sh' with the following content. Or copy from the existing prod server
``` bash
#!/usr/bin/env bash

/home/ubuntu/certbot-auto renew --quiet --no-self-upgrade

sudo cp /etc/letsencrypt/live/portalmbes.com/fullchain.pem /opt/app/chai/volume/config/ssl/fullchain.pem
sudo cp /etc/letsencrypt/live/portalmbes.com/privkey.pem /opt/app/chai/volume/config/ssl/privkey.pem
```
2. Create cronjob
``` bash
crontab -e
Add the following command:
0 0 1 */2 * /home/ubuntu/update-cert.sh
```

#### Install the deployment tool
1. Log in the instance and download the tool
``` bash
curl -L https://github.com/docker/compose/releases/download/1.9.0-rc2/docker-compose-`uname -s`-`uname -m` > docker-compose
```
2. Change the permission
``` bash
chmod +x docker-compose
```
3. Move the tool to bin folder
``` bash
sudo mv docker-compose /usr/local/bin/docker-compose
```

#### Deployment
1. Ask devs for *docker-compose.yml* or copy from the existing prod server,  then place it to user folder, eg. /home/ubuntu.
2. run the command to deploy
``` bash
sudo docker-compose up -d

#### Redeployment
1. Stop the system
``` bash
sudo docker-compose stop
```
2. Update code if necessary
``` bash
sudo docker-compose pull
```
3. Restart the system
``` bash
sudo docker-compose up -d
```
>Redeployment won't delete any existing data in the system