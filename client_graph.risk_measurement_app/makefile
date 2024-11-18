all: riskgraph customer_app workbench_apps

riskgraph:
	sleep 1
	bash -x start-riskgraph

customer_app:
	sleep 1
        cd customer_app ; bash -x customer_app_start 1

workbench_apps:
	sleep 1
        cd cloud-information-genai-workbench ; bash -x workbench-start-cluster 1 
