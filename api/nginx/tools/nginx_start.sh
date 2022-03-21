#!/bin/bash
# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

set -e
TARGET_DIR=/etc/nginx/moviefav/locations

if [ -z "${NGINX_ID}" ]; then
    echo "NGINX_ID not set. Must be one of \"fortress\" or \"toapi\""
    exit 1;
fi
if [ -z "${NGINX_SERVICE_LIST}" ]; then
    echo -n "NGINX_SERICE_LIST must be defined.\n"
    echo -n "Example:\n\n"
    echo "
{\"service_list\":
	{
	  \"fortress\" : [
	  	         {\"foo\":3000},
			 {\"foo2\": 3001}
		       ],
	  \"toapi\" : [
	  	         {\"baz\":9494},
	  	         {\"baz2\":9495},
		      ]
	}
}
"
    exit 1;
fi

#
#
#
echo "Building NGINX Config for ${NGINX_ID}..."

STDOUT_MODE=0
if [ ! -d "$TARGET_DIR" ]; then
    echo "*** Cannot find \"${TARGET_DIR}\" directory."
    echo "*** This is normal if you're ONLY testing this script locally."
    echo "*** Not configuring NGINX. Will skip file creation."
    echo ""
    STDOUT_MODE=1
fi

if [ $STDOUT_MODE -eq 0 ]; then
    rm -f ${TARGET_DIR}/*.conf
fi

#
#
#

function make_entry
{
    service="$1"
    port="$2"


    out="
# Auto generated. Do not edit.
    location /${service}/ {
        proxy_pass http://${service}:${port}/;
        proxy_http_version 1.1;
    	proxy_set_header Host \$host;
    	proxy_set_header X-Real-IP \$remote_addr;
        proxy_redirect off;
        expires -1;
    }
"
    echo "$out";
}


#
#
#

echo "TEST ID=${NGINX_ID}"
echo "TEST NSL=${NGINX_SERVICE_LIST}"

if [ $STDOUT_MODE -eq 0 ]; then
     echo "listen ${NGINX_PORT};" > ${TARGET_DIR}/services.conf
else
     echo "Would write to ${TARGET_DIR}/services.conf"
fi
    
n=0
items=`echo ${NGINX_SERVICE_LIST} | jq  -c '.service_list.'${NGINX_ID}'[]' | tr -d "{" | tr "}" "\n"`

echo "TEST items=${items}"

total=`echo $items | grep ":" | wc -l | awk '{print $1}'`
for item in $items; do
    in_service=`echo $item | awk -F\" '{ print $2 }'`
    in_port=`echo $item | awk -F: '{print $2}'`

    data="$(make_entry $in_service $in_port)"

    echo "Service: $in_service, port $in_port"
    if [ $STDOUT_MODE -eq 0 ]; then
	echo "$data" >> ${TARGET_DIR}/services.conf
    else
	echo "$data"
	echo "--------"
    fi
done;
echo "Done."


#
# Hand off to docker entry point
#
if [ $STDOUT_MODE -eq 0 ]; then
   echo "Handing off to next entry point: $@"
   exec "$@"
else
   echo 
   echo "*** Would hand off to docker entry point here."
fi
exit 0





