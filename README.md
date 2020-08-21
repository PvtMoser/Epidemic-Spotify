# Epidemic-Spotify

Epidemic-Spotify is a Python program to fetch pre-defined Epidemic songs from Spotify and store them in a DB.

## Execution on Linux & Windows

To run the program on linux, use 

```bash
python ./epidemic.py
```

On windows, use 

```bash
python epidemic.py
```

Make sure to have write privileges in the respective directory so the DB and log files can be created. Also make sure to adjust keys.py to use a valid clientID and clientSecret.

## Logging
The file "log.log" will contain detailed logs on what has happened during program execution. A final console print is used to give immediate feedback when executed as a docker. 



## Execution as docker

To run as a docker, build using

```bash
docker build -t epidemic .
```

before executing using

```bash
docker run epidemic
```


## Extension of the DB model

The file "data_model_question_2.pdf" contains ideas on how to extend the data model to depict relationships between songs and playlists, and SQL dummy statements on how to answer specific questions around the relationships. 

