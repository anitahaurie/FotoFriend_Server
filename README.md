# FotoFriend_Server

# **POST StoreImage**
Uploads an image to the user’s account. The image is stored in the s3 bucket and run through the Clarifai prediction model. The keywords found by the prediction model are stored in the database.
**Resource URL**
http://fotofriend.us-west-2.elasticbeanstalk.com/storeImage
**Resource Information**
Response formats: 			HTML Status Code
Requires authentication? 	Yes
**Parameters**
*Name*		*Description*										*Example*
username	User’s Google account name used in authentication	john_doe_1234
image		Image file to upload to the site					.jpeg file

**Example Request**
POST http://fotofriend.us-west-2.elasticbeanstalk.com/storeImage
**Example Response**
200
 

# **POST Login**
Creates a new MongoDB collection for the user if it is the first time logging in. Accesses the user’s database and returns a list of links to the user’s stored images.
**Resource URL**
http://fotofriend.us-west-2.elasticbeanstalk.com/login
**Resource Information**
Response formats: 			JSON Response
Requires authentication? 	Yes
**Parameters**
*Name*		*Description*										*Example*
username	User’s Google account name used in authentication	john_doe_1234

**Example Request**
POST http://fotofriend.us-west-2.elasticbeanstalk.com/login
**Example Response**
{
    "Links": [
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/dog.jpg",
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/dog.jpeg",
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/cat.jpg",
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/bunny.jpg",
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/rabbit.jpg",
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/madcat.jpg",
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/box-turtle.jpg"
    ]
}
 
# **POST Filter**
Receives a list of keywords and returns the image links associated to all keywords.
**Resource URL**
http://fotofriend.us-west-2.elasticbeanstalk.com/filter
**Resource Information**
Response formats: 			JSON Response
Requires authentication? 	Yes
**Parameters**
*Name*		*Description*										*Example*
username	User’s Google account name used in authentication	john_doe_1234
keywords	List of keywords to filter by						[cat, flower]

**Example Request**
POST http://fotofriend.us-west-2.elasticbeanstalk.com/filter
**Example Response**
{
    "Links": [
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/cat.jpg",
        "https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/madcat.jpg",
    ]
}
 
# **POST Delete**
Deletes a specified image.
**Resource URL**
http://fotofriend.us-west-2.elasticbeanstalk.com/deleteImage
**Resource Information**
Response formats: 			HTML Status Code
Requires authentication? 	Yes
**Parameters**
*Name*		*Description*										*Example*
data		Image data											.jpeg raw data
username	User’s Google account name used in authentication	john_doe_1234
url			URL of image to delete								"https://s3-us-west-2.amazonaws.com/foto-friend/59fac5a32bc4643271af86ea/madcat.jpg"

**Example Request**
POST http://fotofriend.us-west-2.elasticbeanstalk.com/deleteImage
**Example Response**
200

