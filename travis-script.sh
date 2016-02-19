#!/bin/sh
echo $TRAVIS_BUILD_DIR
cd $TRAVIS_BUILD_DIR
sudo adduser opentrv --system --disabled-password --uid 510
sudo addgroup --gid 510 opentrv
sudo adduser --uid 510 opentrv --ingroup opentrv sudo
# sudo mkdir /srv/opentrv
sudo chown -R opentrv:opentrv $TRAVIS_BUILD_DIR
sudo mkdir $TRAVIS_BUILD_DIR/database/
sudo mkdir $TRAVIS_BUILD_DIR/logs/
sudo -u postgres psql -c 'create user opentrv --createdb --superuser' 
sudo -u postgres psql -c 'create database opentrv_db owner opentrv'
# sudo cp $TRAVIS_BUILD_DIR/templates/gunicorn.conf.j2 /etc/init/opentrv_gunicorn.conf
# sudo cp $TRAVIS_BUILD_DIR/templates/nginx.conf.j2 /etc/nginx/sites-available/opentrv
# sudo ln /etc/nginx/sites-enabled/opentrv /etc/nginx/sites-available/opentrv
# sudo service nginx restart
# sudo service gunicorn restart
# sudo service udp_server restart
