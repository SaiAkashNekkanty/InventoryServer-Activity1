# src: https://docs.docker.com/engine/network/drivers/overlay/

docker network create \
  --opt encrypted \
  --driver overlay \
  --attachable \
  my-attachable-multi-host-network
