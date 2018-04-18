setup: deps netsim nso

deps:
	pip install -r requirements.txt

netsim:
	ncs-netsim create-network cisco-ios 3 router
	ncs-netsim start

nso:
	ncs-setup --dest .
	ncs

ansible:
	python generate_playbook.py

clean:
	ncs --stop
	ncs-setup --reset
	ncs-netsim stop
	ncs-netsim delete-network
	rm -rf host_vars
	rm -rf netsim packages state target scripts logs ncs-cdb storedstate README.netsim README.ncs ncs.conf