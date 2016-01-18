# TD3_CORPUS

### I . Récupération du corpus + II . Nettoyage du corpus

> Par souci de mémoire on a uploadé que le fichiers nettoyé en utilisant jusText

##### Récupération du corpus et nettoyage en utilisant jusText
```python
get_html_file(listeOfTuples, 'justText')
```
##### Récupération du corpus et nettoyage en utilisant html2Text
```python
get_html_file(listeOfTuples, 'html2text')
```
##### Récupération du corpus et nettoyage en utilisant boilerpipe
> Pour utiliser BoilerPipe il faut installer Java SE6 

```python
get_html_file(listeOfTuples, 'boilerpipe')
```

###III . L'évaluation intrinsèque du corpus
##### Evaluation intrinsèque du corpus
```python
evaluation()
```
##### Evaluation intrinsèque du corpus par langues
```python
evaluation_par_langue_global()
```
##### Evaluation intrinsèque du corpus par domaines
```python
evaluation_domaines()
```

###IV . L'évaluation extrinsèque du corpus
```python
evaluation_extrinseque()
```
