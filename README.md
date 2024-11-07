# insureyourtechcloudgraph
A Cloud Risk - Calculation engine for B2B amnd B2C usage
Public B2C graph in Neo4J - a Graph approach to technology risks and outages
Has Webscraping and automation supported by Gen.AI stack , LLMS, RAGs, Vectors of search , uses Ollama and Llama3.2 on prototype

## Customer B2C Graph - Cloud risk 

Neo4J - client risk Graph : http://localhost:17474

Create with make

```
make riskgraph
```

Customer B2C Sample Graph - overly simplified

![cloud risk example](images/riskgraph.png)
 
### Cloud Information Workbench - GenAi supported collection about Cloud Risk Outages

```
cd cloud-information-genai-workbench
```

---

##  Workbench - App 1 bot  


UI: http://localhost:8501  

- Use Ollama LLm to search for Outages about cloud services
- In example search about AlloyDB outages in GCP cloud

![cloud risk information extraction with pdf-v1-bot](images/bot_app1_workbench.png)
![cloud risk app 1 rag_outage search](images/workbench_app1_outage_search_with_rag_support.png)
![cloud risk app 1 rag_outage search2](images/workbench_app1_rag_enabled.png)


---

##  Workbench - App 3 pdf-bot  


UI: http://localhost:8503  
DB client: http://localhost:7474

- import from PDF files Cloud services information
- Load high ranked cloud outages information
- Extract from PDF to Neo4J Vector information

![cloud risk information extraction with pdf-v1-bot](images/pdf_bot_outage_extract_v1.png)
![neo4j_cloud risk information extraction with pdf-bot](images/extraction_to_neo4j_bot_pdf_bot.png)
	
