// configuration file specific to AWS variables
var deviceId = 'my_rPi'; // replace with your Raspberry Pi ID (defined in rPi capture script)
var tableName = 'mattsona-rpi-camera_metadata'; // replace with your DynamoDB table name
var awsAccessKey = ''; // replace with your access key ID
var awsSecretKey = ''; // replace with your access key secret
var awsRegion = 'us-west-2'; // replace with the region the DynamoDB table resides in 
var cognitoIdentityPool = ''; // TBD
var cognitoUnauthRoleARN = ''; // TBD