# mspec apps
Example applications generated with the [mspec template app generator](https://github.com/medium-tech/mspec).

### setup
To generate apps, setup a venv and install the `mspec` library:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## my-sample-store
The app in `./my-sample-store/app` was created by following the setup instructions above and then:

    cd my-sample-store
    mkdir app
    python -m mtemplate render --spec my-sample-store.yaml --output app

After generating apps cd into `./app/py` and follow the instructions in the readme, then cd into `./app/browser1` and follow the instructions in that readme.