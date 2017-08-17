fname=`date +"%m-%d_%M:%S"`

serverless invoke local -f simpleupload -d \
  "{\"web_location\":\"http://google.com\", \"s3_bucket\":\"gsfdsccdcdsacdsacs\", \"s3_key\":\"google.com\", \"filename\":\"test-s-$fname\"}"

  serverless invoke local -f multipartupload -d \
    "{\"web_location\":\"http://google.com\", \"s3_bucket\":\"gsfdsccdcdsacdsacs\", \"s3_key\":\"google.com\", \"filename\":\"test-m-$fname\"}"
