# web-api

## Contributing

Firstly, thank you!

This project uses `Python 3.6` and `Node 8`. You will also need `Docker` to run the tests.

* Install the Python dependencies annotated in requirements.dev.txt:
```bash
$ pip install -r requirements.dev.txt
```

* Install the Node dependencies:
```bash
$ sudo npm install -g serverless
$ npm install
```

* You'll also need to set up your AWS credentials. Ask your local admin for a set. Store them locally with:
```bash
$ aws configure
```

You can lint the project and run the tests with:
```bash
$ make lint
$ make test
```

You can deploy to the dev environment with:
```bash
make deploy-dev
```
