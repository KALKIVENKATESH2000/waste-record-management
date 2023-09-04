#!/bin/bash
set -x
set -e
STAGE_SRC_DIR="/home/ubuntu/waste-record-management"

m_stage_deployment() {
    ##### changing the owner for the files
     chown -fR  www-data:www-data $STAGE_SRC_DIR/
    #####Coping secret files to api
    #echo ***************coping secure files.......**************************
  #/usr/local/bin/aws s3 cp s3://iidm-env-private/stagingStore.env $STAGE_SRC_DIR/.env

}
m_prod_deployment() {
#   #### changing the owner for the files
     chown -fR  www-data:www-data $STAGE_SRC_DIR/company/httpdocs
#    #####Coping secret files to api
   # echo ***************coping secure files.......**************************
  #/usr/local/bin/aws s3 cp s3://iidm-env-private/prodStore.env $STAGE_SRC_DIR/.env

}
if [ "$DEPLOYMENT_GROUP_NAME" == "WRMdeploymentgroup" ]; then
    echo *************************************Running Deployment***********************************
    m_stage_deployment
fi
if [ "$DEPLOYMENT_GROUP_NAME" == "iidm-prod-store-deployment" ]; then
 ##   echo *************************************Running Deployment***********************************
    m_prod_deployment
fi
