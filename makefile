all: config_where_am_I_running webscraping backend_server customer_app workbench_apps riskgraph

check:
	whoami ; id; pwd; ls -listarh; docker ps
	echo "make check - Warning : Has No specific - rule to make target 'check'.  just continue."

distcheck:
	whoami ; id; pwd; ls -listarh; docker ps
	echo "make distcheck - Warning : Has No specific - rule to make target 'distcheck'.  just continue."

config_where_am_I_running:
	whoami ; id ; pwd ; ls -listarh ; docker ps
	echo "make config_where_am_I_running - Warning : Has No specific - rule to make target 'config_where_am_I_running'.  just continue."

webscraping:
	sleep 1
	cd information/outages/webscraping/outage-webscraping ; bash -x run-webscraping 4 ; cd ../../..
	echo "Webscraping , pdf file samples extracted, built! Now, waits for upload it later in database to be ready."

backend_server:
	sleep 1
	cd cloud-services-risk-ratings-api ; bash -x build-api-cluster 4 ; cd ..
	sleep 90 # wait for the database to be ready

customer_app:
	sleep 1
	cd cloud.risk-customer_portal_app ; bash -x customer_app_start 4 ; cd ..
	sleep 90 # wait for the database to be ready

workbench_apps:
	sleep 1
	# cloud-information-genai-workbench ; bash -x workbench-start-cluster 4 # ; cd ..
	echo "workbench-apps skips from build , too long and big 6GB + 4*18GB disk required to build"

riskgraph:
	sleep 1
	# client_graph.risk_measurement_app ; bash -x start-riskgraph # ; cd ..
	echo "riskgraph skips from build"
