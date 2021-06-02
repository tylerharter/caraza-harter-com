# we want a canvas discussion for every video.  gen-vid-pages.py converts an md (creating one if none exists) for each video to an HTML.  upload-vid-pages creates discussions from these.
gen-vid-pages.py
upload-vid-pages.py

# uploads other files not related to videos (slides, pytutor exercises, worksheets, code, etc)
upload_files.py

# creates modules from files and discussions
gen_modules.py

# cleanup stuff
delete-discussions.py
delete-modules.py
