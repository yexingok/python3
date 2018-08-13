#!/bin/bash

yum update -y
yum install -y httpd curl python-pip screen 
pip install boto3
chkconfig httpd on
service httpd start
region=$(curl -o- -s http://169.254.169.254/latest/meta-data/public-hostname | cut -d. -f2)
AZ=$(curl -o- -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
public_ip=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
INDEX="/var/www/html/index.html"
echo "<h2>Server Details:</h2> </br>" > $INDEX
echo "</br>" >> $INDEX
echo "Region: ${region} </br>" >> $INDEX
echo "AvailbilityZone: ${AZ} </br>" >> $INDEX
echo "Public ip: ${public_ip} </br>" >>  $INDEX
echo "Instance id: ${instance_id} </br>" >>  $INDEX
