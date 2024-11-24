all: config_where_am_I_running backend_server customer_app workbench_apps riskgraph

config_where_am_I_running:
	whoami
	pwd
	ls -listarh

backend_server:
	sleep 1
	cd cloud-services-risk-ratings-api ; bash -x build-api-cluster 4

customer_app:
	sleep 1
	cd cloud.risk-customer_portal_app ; bash -x customer_app_start 4

workbench_apps:
	sleep 1
	# cloud-information-genai-workbench ; bash -x workbench-start-cluster 4
	echo "workbench-apps skips from build , too long and big 6GB + 4*18GB disk required to build"

riskgraph:
	sleep 1
	# client_graph.risk_measurement_app ; bash -x start-riskgraph
	echo "riskgraph skips from build"

