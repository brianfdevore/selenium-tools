To use the Craigslist ad posting tool in this directory, do the following:

1. Run update_regions.py first to fetch the latest CL regions.  This process filters and organizes the regions into a json file which contains the region names and ids needed later for posting.

2. Verify that the images directory contains the correct images, and in the correct order.

3. Review the configuration in ./infiles/ad_config.json for ad creation and modify as needed.

4. Note that Craigslist account credentials and payment card info are stored in AWS SSM.  You must have the AWS CLI installed locally, and have a valid credentials file configured (see "aws configure" command).  The credentials must have appropriate permissions to access SSM to retrieve parameters stored.  You will need to store those parameters initially before using this app (it assumes they are there already).

5. When ready, run post_ads.py to publish the ads.


## Resources ##
WYSIWYG HTML Editor (web-based)
https://html5-editor.net/

