fname=`date +"%m-%d_%M:%S"`

# serverless invoke local -f simpleupload -d \
#   "{\"web_location\":\"http://google.com\", \"s3_bucket\":\"gsfdsccdcdsacdsacs\", \"s3_key\":\"google.com\", \"filename\":\"test-s-$fname\"}"

# serverless invoke local -f multipartupload -d \
#     "{\"web_location\":\"http://google.com\", \"s3_bucket\":\"gsfdsccdcdsacdsacs\", \"s3_key\":\"google.com\", \"filename\":\"test-m-$fname\"}"

BIG_FILE="https://dumps.commonsearch.org/webgraph/201606/host-level/pagerank/pagerank-top1m.txt.gz"

serverless invoke local -f multipartupload -d \
    "{\"web_location\":\"$BIG_FILE\", \"s3_bucket\":\"gsfdsccdcdsacdsacs\", \"s3_key\":\"google.com\", \"filename\":\"test-m-$fname\"}"
