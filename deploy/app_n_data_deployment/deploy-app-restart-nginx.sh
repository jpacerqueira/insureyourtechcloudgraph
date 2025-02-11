#/bin/bash env
#
echo "Redeploy Customer-Portal Apps"
cd ~
cd ~/insureyourtechcloudgraph/cloud.risk-customer_portal_app ; bash -x customer-app-start 4 1 0 
#
echo "Restart NGINX - 30 seconds lag"
cd ~
cd ~/insureyourtechcloudgraph/cloud-services-risk-ratings-api ; docker-compose restart -t 30 nginx-proxy
#
echo "Done! Apps Deployment - from home directory "
#
