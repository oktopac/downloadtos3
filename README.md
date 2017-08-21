# downloadtos3
A serverless utility for downloading files directly to s3 from the web. It uses an AWS lambda function to download a link directly to an AWS S3 bucket without going via your local machine.

# Installation

* Have and configure AWS
* Install [serverless](https://www.serverless.com) 
* run `serverless deploy` in the main directory. Take note of the outputs
* Load the [chrome_extension] into your chrome browser
* Configure the chrome extension by adding in the credentials, region and function name
