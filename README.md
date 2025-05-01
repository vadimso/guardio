PokeAPI Flask App - DevOps Deployment Project

This project is a Python web application using Flask that retrieves data about Pokémon from the public PokeAPI, logs user queries, and is fully automated for deployment via CI/CD, Docker, Kubernetes, HPA, and Monitoring.

Features

Exposes a /pokemon?name=<pokemon_name> endpoint
Returns name, URL, and base stats (HP, Attack, Defense, etc.)
Logs all queries to a query_log.csv file
Containerized with Docker
Deployed to a Kubernetes cluster (e.g., Minikube)
Autoscaled with Horizontal Pod Autoscaler (HPA)
Automated CI/CD pipeline via GitHub Actions
