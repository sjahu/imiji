# imiji
imiji is a basic image repo webapp that I made for Shopify's Summer 2020 Developer Intern Challenge. The name comes from the Korean word for images (according to Google Translate).

Stephen Humphries, 2020

# Features
- Upload one or more images to a gallery
- Add descriptions to images and a title to the gallery
- View an uploaded gallery from a unique link
- Access images directly via their own unique links
- REST API to upload and download images and create galleries

# Access the application
Create a gallery and upload images at http://[server]:[port] and view galleries at http://[server]:[port]/gallery/[id] .

# Configuring dev environment
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
To run the project, run `workon imiji` then `./run.sh`. The default port is 5000. A MongoDB instance must be accessible at the URI specified in the Flask instance config.
