

```
git clone https://github.com/RasaHQ/starter-pack-rasa-nlu.git
```


```
pip install -r requirements.txt
```


```
python -m spacy download en
```




```make train-nlu```  

```make run-nlu```  


```curl -X POST localhost:5000/parse -d '{"query":"Hello", "project": "current"}'```  


