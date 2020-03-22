# imiji
imiji is a basic image repo webapp that I made for Shopify's Summer 2020 Developer Intern Challenge. The name comes from the Korean word for images (according to Google Translate).

Stephen Humphries, 2020

# Configuring environment
## Prerequisites:

- python3
- pip
- virtualenvwrapper
    - `pip3 install virtualenv virtualenvwrapper`
    - Add the following to .bashrc or .bash_profile

`# virtualenvwrapper stuff
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
source /usr/local/bin/virtualenvwrapper.sh`

- cd to the project folder and run `mkvirtualenv -a $(pwd) imiji`
- `pip install flask pymongo`



# Launching imiji
To run the project, execute run.sh.
