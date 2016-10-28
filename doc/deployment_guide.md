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

Please ask devs for *settings.ini*.

#### Sign up Docker Cloud and connect it to AWS EC2 instance created above.
1. Click [here](https://cloud.docker.com/) to navigate to *Docker cloud* official website, then sign up.
2. Config the EC2 instance following [this article](https://docs.docker.com/docker-cloud/infrastructure/link-aws/#/acreate-a-dockercloud-role-role).
3. Log in Docker cloud and get into 'Nodes' menu on the left side. 
4. Click 'Bring your own node' button, it will show you a command, like `curl -Ls https://get.cloud.docker.com/ | sudo -H sh -s 1ec9a8afe1ec424ab49271234567890`
5. Run the command above on the prod instance.

#### Config Docker Cloud to deploy
1. Log in Docker Cloud, get into 'Stack' menu on the left side.
2. Click 'Create' button to create a stack. One stack represents a webapp, it may contains several docker contains.
3. Give it a stack name, and paste stackfile scripts. Please ask devs for scripts.
4. Click 'Create & Deploy' button to finish deployment.

-------------------

**Docker Cloud** can deploy and manage Dockerized applications. It can make you to deploy apps anywhere, simplify docker provisioning, etc. Please click [here](https://www.docker.com/products/docker-cloud#/features) to find the introduction of Docker Cloud.