from pyngrok import ngrok, conf
import os
import yaml

path = os.path.expanduser("/home/user/Projects/keys/ngrok/ngrok.yml")
with open(path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
ngrok_auth_token = config['agent']['authtoken']
confi = conf.get_default().auth_token = ngrok_auth_token
print(confi)
print(config)
print(ngrok_auth_token)