
Working Command Line Chatbot with:
- intent detection
- intent confidence generation
- multiple intent detection
- rasa forms (still working on it)

To build & edit the docs, first install all necessary dependencies:

```
brew install sphinx
pip install -r dev-requirements.txt
```

After the installation has finished, you can run and view the documentation
locally using:
```
make livedocs
```

Visit the local version of the docs at http://localhost:8000 in your browser.
You can now change the docs locally and the web page will automatically reload
and apply your changes.
