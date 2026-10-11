.PHONY: verify lint

verify:            ## ad-hoc verification of scripts/ (exit 0 = pass)
	python3 scripts/verify_scripts.py

lint:              ## syntax-check every script
	python3 -m py_compile scripts/build_project.py scripts/extract_assets.py scripts/prompt_lint.py scripts/shot_log.py scripts/md_to_docx.py scripts/verify_scripts.py
	bash -n scripts/demo_run.sh
	@echo "py_compile ok; demo_run.sh syntax ok"
