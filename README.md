# start.py [![Build Status](https://travis-ci.org/local-motion/playground-importer.svg?branch=master)](https://travis-ci.org/local-motion/playground-importer)

This importer allows to seed our database with playgrounds that have indicated
that they're interested in making venues, such as children playgrounds, smoke-free.

Note - It currently doesn't support auth, so it assumes a `kube port-forward` in case of
non-local environments.

In general, the script:
1. Takes a playground Xlsx file
1. Turns it into JSON
1. For each playground
    1. Creates a playground in Local Motion (requires env `ONBOARDING_API`)



## Docker
### Run it as an executable (not a service)
```
docker run --rm -v $(PWD)/samples:/imports -v $(PWD)/html_templates:/html_templates \
    -e ONBOARDING_API=http://localhost:8082/playgrounds \
    localmotion/playground-importer \
    $(whoami)_docker
    /imports/1_playground.xlsx
```

### Build Docker image from source
```
docker build -t localmotion/playground-importer .
```


## Command line

### Install dependencies
To setup:
```
virtualenv -p python3 playgrounds
source playgrounds/bin/activate
pip install -r requirements.txt
```

### Configure
Then to subsequently add the following to a local `.env` file. Enable Mailchimp and Sentry
integrations by setting respective env variables.
```
ONBOARDING_API=http://localhost:8082/playgrounds

# Sentry.io configuration
SENTRY_DSN=
```

### Run it from command line
Make sure you switched to the correct `virtualenv`:
```
source playgrounds/bin/activate
```

And then simply run:
```
python start.py $(whoami)_automated $(pwd)/samples/1_playground.xlsx 
```

### XLSX import samples
Samples can be found at [Samples](./samples) in this repository.
 