1. Disable Login/Signup links in `base.html` template and deploy
2. Disable Archive Menu Item via CMS admin
3. Create folder `pyconsg2/pyconsg2/static/archive/YYYY`
4. `cd` into that folder
5. Now run wget:

wget \
     --recursive \
     --no-clobber \
     --page-requisites \
     --html-extension \
     --convert-links \
     --restrict-file-names=windows \
     --domains pycon.sg \
     --no-parent \
         https://pycon.sg

6. Commit the new files
7. Re-enable Login/Signup links in `base.html` and add CMS page for the new YYYY
   archive.
