build:
	docker-compose build

server:
	docker-compose up -d python_server
	docker-compose logs -f python_server

client:
	docker-compose run --rm python_client

up:
	docker-compose up -d python_server
	docker-compose run --rm python_client

down:
	docker-compose down --volumes --remove-orphans

clean:
	docker-compose down --rmi all --volumes --remove-orphans
