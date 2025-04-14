# sc-retails

### [Archived]
A script to scrape photos, item names and price from reknowned supremecommunity.com

### [Update 2021]
- [x] refined HTML selectors
- [x] Added verification skip for HTTPS Requests
- [x] Added date-based folder structure for images
- [x] Added module to upload scraped items to google sheets
    - create token and credentials and input into `credentials.json`
    - create a google sheets and input to the script.
    - configure starting cell in the google sheets


### See V1 in action :robot:

![V1 working]("examples/sc-retails working video.gif")

### Requirements
Python 3
```
pip install -r requirements.txt
```

else do `python -m pip install` on the missing packages


run `python sc.py`

input link.

written by yours truly. ymmxl

