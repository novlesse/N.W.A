<br>
<h1 align="center">A u d i o l o g y</h1>
<h2 align="center">COMP 2523 - Object Oriented Programming</h2>
<h3 align="center">FINAL PROJECT : Apple Music Clone</h3>

<p align="center">
<img src="image_assets/audiologyLogoClear.png">
</p>

<h2 align="center">N.W.A</h2>
<h2 align="center">Nerds With Attitdude</h2>
<h4 align="center">By: John Nguy | Emmy Wong | Jeffrey Lau</h4>
<br><br>

1. Setup an AWS S3 account if you haven't already done so. 

> https://aws.amazon.com/s3/

2. Create a bucket along with the following directory:

> your_bucket_name/uploads

3. run the following command in your terminal:

> aws configure

4. Enter the values below for the following prompts:

> AWS Access Key ID: YOUR_ACCESS_KEY
> AWS Secret Access Key: YOUR_SECRET_KEY
> Default region name: us-west-1
> Default output format: json

5. Go to your S3 console https://s3.console.aws.amazon.com/

6. Click on your bucket --> Permissions --> Bucket Policy

7. Enter the following code to make your bucket public to access uploaded audio files:

***Note:*** Replace `bucketname` with your bucket name.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucketname/*"
        }
    ]
}
```

8. Hit save.


#### Run:

> python3 run.py

<br>

## License & Copyright

Copyright (c) 2020, John Nguy, Emmy Wong, Jeffrey Lau

Licensed under the [MIT License](license.md).
