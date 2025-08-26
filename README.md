# mspec apps
Example applications generated with the [mspec template app generator](https://github.com/medium-tech/mspec)

### setup
To setup this repo to generate the templates apps:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install mspec

## my-sample-store
The app in `./my-sample-store/dist` was created by following the setup instructions above and then:

    cd my-sample-store
    python -m mtemplate render --spec my-sample-store.yaml --output dist

To run the apps see *run and test generated apps* section in [mspec repository](https://github.com/medium-tech/mspec) readme.