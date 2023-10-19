import subprocess
import sys

container_name = sys.argv[1] + "_service"
image_name = container_name + "-image"
subprocess.call((f'docker-compose stop {container_name}'))
subprocess.call((f'docker-compose rm -f {container_name}'))
subprocess.call((f'docker rmi -f {image_name}'))
subprocess.call((f'docker-compose up -d'))