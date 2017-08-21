document.forms[0].onsubmit = function(e) {
    e.preventDefault(); // Prevent submission
    console.log("submitting form");
    var AWS_ACCESS_KEY = document.getElementById('AWS_ACCESS_KEY').value;
    var AWS_SECRET_KEY = document.getElementById('AWS_SECRET_KEY').value;
    var S3_BUCKET = document.getElementById('S3_BUCKET').value;
    var LAMBDA_FUNCTION_NAME = document.getElementById('LAMBDA_FUNCTION_NAME').value;
    var REGION = document.getElementById('REGION').value;
    chrome.runtime.getBackgroundPage(function(bgWindow) {
        bgWindow.setAWSCreds(AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET,
          LAMBDA_FUNCTION_NAME, REGION);
        window.close();     // Close dialog
    });
};
