.PHONY: clean
clean:
	rm -rf docs/build/html

.PHONY: docs
docs:
	sphinx-build -b html docs/source/ docs/build/html

.PHONY: precommit
precommit:
	python precommit.py