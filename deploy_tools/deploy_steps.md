# Steps followed in OTTG chapter 8

## Provisioning
1. Assume we have a user account and home folder
2. `sudo apt-get install nginx git python-pip`
3. `sudo pip install virtualenv`
4. Add Nginx config for virtual host

    * see *nginx.template.conf*
    * replace `SITENAME` with, eg, *staging.my-domain.com*

5. Add Upstart job for Gunicorn

    * see *gunicorn-upstart.template.conf*
    * replace `SITENAME` with, eg, *staging.my-domain.com*

## Deployment
1. Create directory structure in *~/sites*
    * we have a user account at /home/username
    * ```shell
      /home/username
      └── sites
      └── SITENAME
            ├── database
            ├── source
            ├── static
            └── virtualenv
        ```
2. Pull down source code into folder named *source*
3. Start `virtualenv` in `../virtualenv`
4. `pip install -r requirements.txt`
5. `manage.py migrate` for database
6. `collectstatic` for static files
7. Set `DEBUG = False` and `ALLOWED_HOSTS` in *settings.py*
8. Restart Gunicorn job
9. Run FTs to check everything works

# Running fabric
1. open the git-aware windows shell `C:\Program Files\Git\git-cmd.exe`
2. `activate fabric` to use the installed `conda env`
3. `cd $TEST_GOAT_HOME/source/deploy_tools/`
3. `fab deploy:host=laurence@superlists-staging.tinglingham.co.uk`
