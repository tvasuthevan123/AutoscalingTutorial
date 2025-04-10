# Pre-requisites

You must have a MacOSX or Linux device for these instructions to work!

1. Install minikube onto your computer [here](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download) and start a cluster by calling `minikube start`. You will also need **kubectl** installed. Optionally, you should install k9s to follow with the steps to monitor the cluster easier.

2. Install rabbitmq onto your cluster by running the steps from [here](https://www.rabbitmq.com/kubernetes/operator/quickstart-operator#install-the-rabbitmq-cluster-operator)

3. Setup a rabbitmq cluster on your cluster by running the steps [here](https://www.rabbitmq.com/kubernetes/operator/quickstart-operator#hello-rabbitmq)

4. Portforward the rabbitmq cluster service (port 15672 and port 5672) to your localhost so you can access the UI from your browser http://localhost:15672 and to allow the sender script to put messages on the bus. It's easiest if you have `k9s` installed, so you can more easily portforward the rabbitmq service created by following the tutorial link above.

- navigate to the `hello-world` service
- press `shift+f`
- choose the correct ports and portforward

5. Install KEDA onto your cluster by running the steps from [here](https://keda.sh/docs/2.16/deploy/#install-2)

6. Install uv on your machine [here](https://docs.astral.sh/uv/getting-started/installation/#installing-uv)

7. Set environment variables in the terminal as follows (method varies based on the shell you are using)

```bash
RMQ_IP="localhost"
RMQ_USER=(eval kubectl get secret hello-world-default-user --template='{{.data.username | base64decode}}')
RMQ_PASS=(eval kubectl get secret hello-world-default-user --template='{{.data.password | base64decode}}')
```

# Instructions

1. Create a docker image locally by entering the minikube's docker runtime and building the image. This ensures that the cluster does not need to pull the image when it creates the deployment.

```bash
eval $(minikube docker-env)
docker build -t autoscalingtutorial -f consumer.Dockerfile .
```

2. Setup the secrets required for the deployment to work

```bash
kubectl apply -f deployment/rmq_secret.yaml
```

3. Create a deployment for the consumer by running

```bash
kubectl apply -f deployment/deployment.yaml
```

You can verify logs through k9s to see if the consumer is running correctly

4. Execute the sender script by running:

```bash
uv run src/autoscalingtutorial/sender.py
```

If the portforwarding hasn't worked or you haven't set the environment variables up correctly, you may get a connection error to the queue.

5. Change the number of iterations in the sender script to a larger number (2000-5000)

6. Add your scaled object

```bash
kubectl apply -f deployment/scaled-object.yaml
```

7. Rerun step 4 and monitor the number of pods the consumer pod spins up - it will gradually increases as it tries to get through all the messages!
