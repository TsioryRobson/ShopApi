.PHONY: test test-fast test-cov test-auth test-setup

test-setup:
	bash tests/run_tests.sh --deps-only

test:
	bash tests/run_tests.sh -v

test-fast:
	bash tests/run_tests.sh -q

test-cov:
	bash tests/run_tests.sh --cov -q

test-auth:
	bash tests/run_tests.sh tests/test_auth.py -q
