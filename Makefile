# ┌───────────────────────────────────────────────────┐
# │              cross project commands               │
# └───────────────────────────────────────────────────┘
.PHONY: up down show-containers
up:
	docker compose up
down:
	docker compose down
show-containers:
	docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# ┌───────────────────────────────────────────────────┐
# │           nginx_log_parser_dj commands            │
# └───────────────────────────────────────────────────┘
.PHONY: up-nginx_log_parser_dj parse_log
up-nginx_log_parser_dj:
	docker compose up nginx_log_parser_dj
parse_log:
	docker exec -it nginx_log_parser_dj python manage.py parse_log $(url)

.PHONY: makemigrations migrate  runserver sqlmigrate shell
makemigrations migrate runserver sqlmigrate shell:
	docker exec -it nginx_log_parser_dj  python manage.py $@




