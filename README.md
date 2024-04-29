# Nova

## Get started
Install the following

- Django
- folium
- ollama
- pangea-django
- pangea-django
- twilio
- segno


Generate custom tokens for
- twilio
- perplexity API
- pangea
(This step is mandatory)

Add the tokens in either .env file or in vault. Update the code correspondingly

Then do
```
python manage.py makemigrations
python manage.py migrate
```

To start the server, run the following
```
python manage.py runserver
```