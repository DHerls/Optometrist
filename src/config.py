import yaml

with open("models.yml") as f:
    model_config = yaml.safe_load(f)

OPENAI_API_KEY = model_config['models']['openai']['api_key']
