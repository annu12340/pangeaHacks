# Nova

## Get started
Install the following

- Django
- folium
- ollama
- pangea-django
- pangea-sdk
- twilio
- segno


Generate custom tokens for
- twilio
- perplexity API
- pangea

All the 3 tokens are manadatory

Add the tokens in either .env file or in vault. Update the code correspondingly

Once that is done, then do
```
python manage.py makemigrations
python manage.py migrate
```

To start the server, run the following
```
python manage.py runserver
```
