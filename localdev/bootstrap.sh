#!/usr/bin/env bash

# This section contains arguments specific to the new instance we are starting
dev_host="192.168.56.1"
testserver_port="3007"
mongodb_port="27017"

start_time="$(date +%s)"

# Step 1. Start MongoDB (script copied from ../mongodb/localhost/bootstrap.sh. TODO: should generate this script)

#!/usr/bin/env bash

# Import the 10gen public GPG Key
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

# Create a /etc/apt/sources.list.d/10gen.list file
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list

# Reload the repository
apt-get update

# Install the latest stable version of MongoDB
apt-get install mongodb-10gen

# Try to repair MongoDB in case we're recovering from an abrupt shutdown or crash
sudo -u mongodb mongod --repair --dbpath /var/lib/mongodb/
sudo service mongodb start

# Step 2. Start Dispatch server

apt-get update

# load the run-time prereqs
apt-get install -y      nginx
echo "apt-get installed nginx"

# create the ngnx config file 
echo "
server {
        listen          80;
        error_log /var/log/nginx/error.log;
        sendfile off;

        # tutorial static files
        location ~ ^/clientlib/ {
            proxy_pass http://$dev_host:$testserver_port;
            }
        
        # tutorial micro-app
        location ~ ^/tt($|_tracking|_history|/) {
            set \$h \$http_host;
            if (\$http_ce_resource_host) {
                set \$h \$http_ce_resource_host;
                }
            proxy_set_header CE-Resource-Host \$h;
            proxy_pass http://$dev_host:$testserver_port;
            }       

    }" > /etc/nginx/conf.d/dispatcher.conf

echo "created /etc/nginx/conf.d/dispatcher.conf"
rm -f /etc/nginx/sites-enabled/default

# (re)start the nginx service
service nginx restart

elapsed_time="$(($(date +%s)-start_time))"
echo "elapsed time: ${elapsed_time} seconds"
