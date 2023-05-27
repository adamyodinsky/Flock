

up:
	docker-compose up -d

down:
	docker-compose down

tear-down:
	docker-compose down -v

logs:
	docker-compose logs -f

minikube-start:
	minikube start --ports=127.0.0.1:443:443 --ports=127.0.0.1:80:80 --ports=127.0.0.1:27017:27017 --ports=127.0.0.1:32017:32017

k8s-up:
	kubectl apply -f k8s/