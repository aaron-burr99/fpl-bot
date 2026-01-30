build:
	docker build -t fpl-bot .

run:
	docker run -d --env-file .env fpl-bot



