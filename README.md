### Point 1 - Docker Image creation process
The code is in the 01 folder
1. We'll use an official docker image with the persistent tag (1.19.6) as our source image
   - Because it is a new solution and we want our image footprint to be as small as we can. we'll use the latest `alpine` based image 
2. Create `index.html` with DATE/TIME settings
3. Running nginx as a non-root user
   - Create an `nginx.conf` file and copy it to the Target image
   - Change Listener port from 80 => 8080 in `default.conf` file (this because we want to run as a not-root user (in our case `nginx`))
   - For the healthcheck (will be used in Liveness/Readiness probes) we'll expose `/healthz` path in `default.conf` file
   - Change docker image context from `root` to `nginx` user (so user which attach to container will be attached as user with limited permissions)

### Point 2 - Pushed as `adamkpn/nginx-datetime`
Docker build instructions:
```bash
docker login
docker build -t adamkpn/nginx-datetime:1.0.1 .
docker push adamkpn/nginx-datetime:1.0.1
```

### Point 3 - With Kustomize 
The code is in the 03 folder
1. The solution contains two environments, `qa` and `production`
2. `qa` example:
```bash
# Bootstrap k3d cluster (this will also expose Ingress on ports 80/443) 
k3d cluster create \
--agents 2 \
--port "80:80@loadbalancer" \
--port "443:443@loadbalancer"

# Create qa namespace
kubectl create ns qa

# Switch to qa namespace
kubectl config set-context $(kubectl config current-context) --namespace qa

# Navigate into the 03/_manifests file
cd 03/_manifests

# Deploy the manifest by running:
kustomize build qa/base | kaf -

# This will deploy the following resources:
- Deployment
- Service
- Ingress
```
3. Add `127.0.0.1  datetime-qa.example.com` record if you want to test the service with the ingress edpoint.
   - To test, open the browser and navigate to http://datetime-qa.example.com/ or https://datetime-qa.example.com/
4. If you want to test the service Internally from the Kubernetes cluster, run the following command:
```bash
kubectl run curl -it --rm --restart=Never --image curlimages/curl -- datetime
```
5. You can repeat the process in an additional namespace production 
- In this case the Ingress Hosts will have name `datetime-production.example.com`

### Point 4 - With Python
The code is in the 04 folder
- this part is not completed yet, will be updated...