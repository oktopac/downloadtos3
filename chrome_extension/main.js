downloadToS3 = function(url) {
  console.log("Downloading url " + url);
  // Get the credentials for the AWS client
  chrome.storage.local.get('aws-creds', function(result) {

    var creds = result['aws-creds'];

    if ( creds.hasOwnProperty('AWS_ACCESS_KEY') && creds.hasOwnProperty('AWS_SECRET_KEY') ) {
      console.log(creds);
      var lambda_name = creds['lambda_name'];
      var s3_bucket = creds['s3_bucket'];
      var region = creds['region'];

      var config = new AWS.Config({
        accessKeyId: creds['AWS_ACCESS_KEY'],
        secretAccessKey: creds['AWS_SECRET_KEY'],
        region: creds['region']
      });

      var lambda = new AWS.Lambda(config);

      lambda_payload = {
        web_location: url,
        s3_bucket: s3_bucket
      };

      lambda_invoke = {
        FunctionName: lambda_name,
        InvocationType: 'RequestResponse',
        Payload: JSON.stringify(lambda_payload)
      }

      console.log("Invoking lambda function");
      console.log(lambda_invoke);

      lambda.invoke(lambda_invoke, function(error, data) {
        if (error) {
          alert(error);
        } else {
          pullResults = JSON.parse(data.Payload);
        }
      });

    }
    else {
      alert("Please configure your authentication tokens at about://extensions");
    }

  })

}

function downloadToS3Link(object) {
  downloadToS3(object['linkUrl']);
}

chrome.contextMenus.create({
  title: "Download to S3",
  contexts:["selection"],
  onclick: downloadToS3Link
});

function setAWSCreds(AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET,
  LAMBDA_FUNCTION_NAME, REGION) {

  chrome.storage.local.set({'aws-creds': {
    "AWS_ACCESS_KEY": AWS_ACCESS_KEY,
    "AWS_SECRET_KEY": AWS_SECRET_KEY,
    "region": REGION,
    "lambda_name": LAMBDA_FUNCTION_NAME,
    "s3_bucket": S3_BUCKET
  }}, function() {
    console.log("Saved new credentials");
  })
}
