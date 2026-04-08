

# Resume Pipeline

## Summary 
This is end-to-end data project, I started because I didn't want to keep apply for jobs that didn't match my resume. This projects aims to simplify the heavy lifting for me and evaluate what job match the skills on my resume and then determine whats jobs, I should apply to.

Using `web scrapping`, Huggingfave `AI model`, ranking system and `MYSQL`, while also building a `pipeline` to run and determine which jobs I should apply to. 



job-resume-pipeline/
├── config/
│   └── config.yaml            # DB creds, categories, API keys (use secrets later)
├── src/
│   ├── __init__.py
│   ├── config.py	      # still waiting 
│   ├── database.py          # SQLAlchemy models + connection
│   ├── main.py				# Main Python file
│   ├── scraper.py			# not yet filled
│   └── storage.py			# not yet filled 
│   			
├── mysql-connection 		# store all details for connecting to the database
├── pyproject.toml				# Place holder
├── .env                     # (gitignored) for secrets
└── README.md				# ReadMe File


### Agenda
- [x] Create a python script 
- [x] Create a MYSQL database
	- [ ] Test python and database connection (In Progress)
- [ ] Use a HuggingFace AI Model
- [ ] Create a Pipeline to run everything

Bonus : 
- [ ] Build a Dashboard of job that shows everything.




