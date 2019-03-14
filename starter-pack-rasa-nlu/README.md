

```
git clone https://github.com/RasaHQ/starter-pack-rasa-nlu.git
```

After you clone the repository, a directory called starter-pack-rasa-nlu will be downloaded to your local machine. It contains all the files of this repo and you should refer to this directory as your 'project directory'.


```
pip install -r requirements.txt
```


```
python -m spacy download en
```




```make train-nlu```  

```make run-nlu```  


```curl -X POST localhost:5000/parse -d '{"query":"Hello", "project": "current"}'```  


