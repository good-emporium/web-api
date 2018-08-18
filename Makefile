deploy-dev:
	serverless deploy --verbose --stage v0-dev

lint:
	pylint functions

test:
	docker run --name ddb -d -p 8000:8000 cnadiminti/dynamodb-local:latest
	sleep 5
	-pytest
	docker stop ddb
	docker rm ddb
