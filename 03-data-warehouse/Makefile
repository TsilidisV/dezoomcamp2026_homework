.PHONY: demo infra-up infra-down kestra-up wait-for-kestra kestra-flow generate-env terraform-apply

# Variables
TF_DIR = infrastructure
KEYS_DIR = $(TF_DIR)/keys
KEY_FILE = $(KEYS_DIR)/service-account.json

# -----------------------------------------------------------
# Main Commands
# -----------------------------------------------------------


demo: infra-up kestra-up wait-for-kestra kestra-flow

infra-up: terraform-apply generate-env

kestra-up:
	@echo "🐳 Starting Kestra..."
	docker-compose up -d
	@echo "✅ Kestra is running at http://localhost:8080"

kestra-flow:
	curl -u "admin@kestra.io:Admin1234" -X POST \
	http://localhost:8080/api/v1/executions/zoomcamp.homework.3/batch-runner

wait-for-kestra:
	@echo "⏳ Waiting for Kestra to be healthy..."
	@bash -c 'until curl -u "admin@kestra.io:Admin1234" --output /dev/null \
		--silent --head --fail http://localhost:8081/health; do \
		printf "."; \
		sleep 5; \
	done'
	@echo "\n✅ Kestra is ready!"



infra-down:
	@echo "💥 Destroying Infrastructure..."
	terraform -chdir=$(TF_DIR) destroy -auto-approve
	rm -f .env

# -----------------------------------------------------------
# Helper Targets (Internal steps)
# -----------------------------------------------------------

terraform-apply:
	@if [ ! -f "$(KEY_FILE)" ]; then \
		echo "❌ Error: $(KEY_FILE) not found. Please place your GCP JSON key there."; \
		exit 1; \
	fi
	@echo "🚀 Initializing and Applying Terraform..."
	terraform -chdir=$(TF_DIR) init
	terraform -chdir=$(TF_DIR) apply -auto-approve

generate-env:
	@echo "🔗 Generating .env file for Kestra..."
	@echo "ENV_GCS_BUCKET=$$(terraform -chdir=$(TF_DIR) output -raw bucket_name)" > .env
	@echo "SECRET_GCP_CREDS=$$(cat $(KEY_FILE) | tr -d '\n' | base64 -w 0)" >> .env
	@echo "✅ .env file generated successfully!"