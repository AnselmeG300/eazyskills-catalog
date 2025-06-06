import os
import sys
import yaml
from glob import glob
from collections import defaultdict

# Define the allowed technologies
ALLOWED_TECHNOLOGIES = {
    # Programming languages
    "python", "java", "c", "c++", "c-sharp", "javascript", "typescript", "ruby",
    "php", "go", "rust", "kotlin", "swift", "scala", "perl", "dart",
    # Containerization and orchestration
    "docker", "podman", "kubernetes", "openshift", "docker-compose",
    "cri-o", "containerd", "helm", "rancher", "docker-swarm", "private-registry",
    # Cloud computing
    "aws", "azure", "gcp", "ibm-cloud", "oracle-cloud", "alibaba-cloud",
    "ec2", "s3", "rds", "eks", "lambda", "azure-vm", "azure-functions",
    "cloud-run", "firebase", "cloudflare", "azure-devops", "aws-cdk", "aws-sdk", "aws-cli",
    # Databases
    "postgresql", "mysql", "mariadb", "sql-server", "oracle-db",
    "mongodb", "cassandra", "dynamodb", "redis", "couchbase", "neo4j",
    "arangodb", "influxdb", "prometheus", "timescale",
    # DevOps and infrastructure
    "terraform", "ansible", "chef", "puppet", "packer", "vault", "consul",
    "jenkins", "gitlab-ci", "github-actions", "spinnaker", "argo-cd", "flux",
    "jenkins-x", "argo-cd", "crossplane", "vcluster", "dapr", "sonarcloud",
    # Security
    "nmap", "wireshark", "burp-suite", "metasploit", "nessus",
    "kali-linux", "trivy", "fail2ban",
    # Monitoring and observability
    "grafana", "datadog", "splunk", "new-relic", "elasticsearch", "kibana",
    "fluentd", "opentelemetry", "jaeger", "loki", "alertmanager",
    # Web development
    "react", "angular", "vue", "svelte", "nextjs", "nuxtjs", "tailwindcss",
    "bootstrap", "material-ui", "express", "django", "flask", "fastapi",
    "spring", "laravel", "rails", "asp-net",
    # AI and machine learning
    "tensorflow", "pytorch", "keras", "scikit-learn", "numpy", "pandas",
    "opencv", "huggingface", "mlflow", "kubeflow",
    # Big data
    "hadoop", "spark", "kafka", "hive", "pig", "flink", "presto", "dremio",
    # Operating systems
    "linux", "windows", "macos", "ubuntu", "centos", "debian", "fedora",
    "redhat", "alpine",
    # Versioning and collaboration tools
    "git", "github", "gitlab", "bitbucket", "mercurial", "svn", "jira",
    "trello", "confluence", "slack", "teams", "github",
    # Software testing tools
    "postman", "xray",
    # Management tools
    "jira",
    # Data tools
    "power-bi", "excel", "power-query", "sql", "snowflake", "teradata", "talend",
    "tableau", "tableau-desktop",
    # Network tools
    "cisco", "packet-tracer",
    # domain
    "it",
    
}

def validate_technologies(technologies):
    """Ensure technologies are in the allowed list."""
    invalid_technologies = [tech for tech in technologies if tech not in ALLOWED_TECHNOLOGIES]
    return invalid_technologies

def validate_file(file, required_fields, category, names_seen):
    """Validate a single YAML file."""
    errors = []
    with open(file, "r") as f:
        try:
            data = yaml.safe_load(f)

            # Validate common fields for all categories
            for field in required_fields:
                if field not in data:
                    errors.append(f"{file}: Missing field '{field}'")

            # Validate technologies (specific to courses)
            if category == "courses" and "technologies" in data:
                invalid_technologies = validate_technologies(data["technologies"])
                if invalid_technologies:
                    errors.append(f"{file}: Invalid technologies - {', '.join(invalid_technologies)}")

            # Validate uniqueness of 'name'
            if "name" in data:
                name = data["name"]
                if name in names_seen:
                    errors.append(f"{file}: Duplicate name '{name}' found in {names_seen[name]}")
                else:
                    names_seen[name] = file

            # Additional validation for FAQ
            if category == "faqs":
                if "questions" in data:
                    if not isinstance(data["questions"], list) or not all(isinstance(q, str) for q in data["questions"]):
                        errors.append(f"{file}: 'questions' must be a list of strings")
                else:
                    errors.append(f"{file}: Missing 'questions' field")

        except yaml.YAMLError as e:
            errors.append(f"{file}: YAML parsing error - {e}")

    return errors

if __name__ == "__main__":
    errors = []
    names_seen = defaultdict(str)  # To track 'name' uniqueness across files

    # Define required fields by category
    required_fields = {
        "courses": ["name", "url", "duration_hours", "level", "objectives", "description", "technologies", "language", "deprecated"],
        "paths": ["name", "target_role", "course_ids", "language", "deprecated"],
        "bootcamps": ["name", "target_role", "modules", "duration_weeks", "language", "deprecated"],
        "faqs": ["url", "questions"]
    }

    # Validate content for each category
    for category, fields in required_fields.items():
        directory = category
        files = glob(f"{directory}/*.yaml")
        for file in files:
            errors += validate_file(file, fields, category, names_seen)

    if errors:
        print("Invalid file content detected:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("All file contents are valid.")
