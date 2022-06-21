# STARS-API

Web API for STARS Explorer to retrieve, process, and share data analysis result, which based on STARS (The Sustainability Tracking, Assessment & Rating System, https://stars.aashe.org/)

## Routes

All routes return Json

- GET  `/`: Root route shows if Web API is running
- GET  `api/v1/rank/[field]`: Get rank by field
- GET  `api/v1/textcloud/[field]`: Get token of textcloud by field
- GET  `api/v1/rank/[field]&[query]`: Get cosine similarity score of specified field with query.

## Install

Install this application by cloning the *relevant branch* and use bundler to install specified gems from `Gemfile.lock`:

```shell
$ python3 -m pip install -r requirements.txt
```

## Execute

Launch the application using:

```shell
export FLASK_APP=api
flask run
```
