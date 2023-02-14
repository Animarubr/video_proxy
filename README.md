# Video Proxy

### Video proxy to bypass servers that uses referrer to block request out of the original site

##### I am using pipenv with my virtual environment manager, you can use others like venv for example

## Installation

```
To Install pipenv
    pip intall pipenv

To intall dependencies
    pipenv install -r requirements.txt
```

## To Run

```
    uvicorn main:app
```

## Basic Use

### To work correctly you need to follow these

#### 1. Create a JWT token, in your main API, with the following parameters

```
{
    url: "url for the video server",
    ref: "referer of original page on video is hosted"
}
```

### 2. Send the JWT to */proxy?token=your_token_here*

#### After the steps. You will receive chunks of the media in your player, by the status code `206`

##### You can change *user_agent* list and *chunk_size* value of the generator in `app.models.stream.py`
