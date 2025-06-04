### Objective

1. Understanding what is Kubernetes?
2. Kubernetes Architecture
3. Main Kubernetes Components
4. Hands on Demo Project

### Kubernetes Summary

1. Kubernetes is a container orchestration framework. It was originally developed by Google.
2. It manages containers like Docker containers.
3. It helps manage applications that are madeup of multiple containers.
4. Helps you deploy containers in Physical, Virtual, Hybrid or Cloud Environments.
5. The rise of microservices led to the *container technology.*
6. Managing loads of containers separately can be difficult and complex, therefore using a technology like Kubernetes helps manage them easily.
7. Advantages of Kubernetes: 
	a. High availability: *Does not have any down time.*
	b. Scalability: Flexible to load of traffic and usage.
	c. Disaster Recovery: *This allows you to recover and restore your data incase of a disaster or malfunction of machines.*
8. **Kubernetes Cluster:** is made up of atleast 1 master node, and multiple worker nodes.
9. **Node:** Each node has a Kubelet process running on it.
10. **Kubelete:** Helps to communicate between the nodes.
11. Applications are running in your ***worker nodes.***
12. **Master nodes:** Runs api servers that is the entry point to the Kubernetes Cluster.
	a. Api Server
	b. Controller Manager
	c. Scheduler
	d. Etcd: This holds the current state of the cluster. It contains all the configuration data.
13. **Virtual Network:** This enables the apis, worker nodes and master node to interact with each other.
14. Worker nodes uses up the most process resources.
15. **Pod:** Is the smallest unit of Kubernetes. A pod generally runs a single application inside its container. Each pod gets its own IP address.
16. You can have multiple or a helper application inside a pod only if its necessary and a requirement which means that both the applications will get their own ip addresses. But incase if one of the apps dies, or the node dies due to a malfunction in services or processes, then a ***New pod will be created*** which will assign a new IP address to the applications. That means you will manually have to replace the ip address with the new one in order to ensure communication between the 2 apps continues. But automate this, there is a layer of a component called ***Services.***
17. **Service and Ingress:** Service has a static or a permanent IP address, so even if the pod dies, the service IP remains the same, and you won't have to change the ips of the pod apps. 
18. The lifecycle of a Pod and Service are not connected, so incase of a Pod failure or malfunction, the service will remain.
19. Accessing your application: The way to do this is through a Web page, which means that you will have to create an external IP address, and exposing your Database would be insecure, so you can have an internal IP address assigned to it. But that is not so practical, because in kubernetes the Web address of the webpage may look like an *ip address of the node followed by the port number of the service.* As a solution, Kubernetes has a layer called ***ingress***
20. Conventionally, if you wanted to change the *endpoint of the database* website url, that would require you to rebuild the application, push the updated code to git, and then rebuild the images which is a tedious task, therefore as a solution, Kubernetes has a layer/component called ***Config map + Secrets***
21. The config map contains all of the information and data related to the pod and service, and all you have to do is change the *database web url/endpoint* on the config map and nothing else. However, if you want to change the credentials of your database, it wouldnt be safe to apply them on the config map, therefore there is a component called ***Secrets.*** It is used to store credentials in base64 format, Kubernetes uses 3rd party tools to further more encrypt to make them more secure.
22. You can access your *config map + secret* using Environment Variables.
23. Data storage: If your pod contains all the data, it would be insecure because in the event of a failure of the pods, the data will be gone and deleted. As solution, Kubernetes has a component called the ***Volume.*** This allows you to allocate physical memory storage within the node, or remote cloud storage.
24. **Deployment and Statefulness:** If a pod application dies, then the users will experience a downtime, in order to avoid this, kubernetes has a component that helps in ***replicating a pod*** and a layer called ***load balancer*** that ensures that the application is up and running even if a node is non functional, so that the user does not experience any downtime. The replica uses the same Service in deploying a new pod using the same Static IP.
25. **Deployment:** This allows you to define the *blue print* for a *pod* and also define how many nodes need to be running at a time, better known as ***replicas***, which ensures the defined number of pods are always running. Incase if a single node dies, it will balance the load by deploying a new pod automatically.
26. **Statefulset:** This is another feature of Kubernetes that allows you to ensure that the database maintains its state because you cannot create replicas of a database, it can lead to database inconsistency, because it would be difficult to track which pod is writing new data in the DB, and which pod is just reading from it. *Databases of mySQL, mongodb and other frameworks should be created using **statefulsets** and not deployments.*
27. Managing database Statefulsets can be a tedious task in order to ensure data synchronisation and consistency is acheived, therefore as a best practice, it works better to deploy ***stateless applications*** inside the cluster and maintaining a database outside the ***kubernetes cluster.***
28. How do we create a Kubernetes Cluster? *All the configuration goes through the masternode apis. Kubernetes dashboard could be a UI, A Script, A Command line tool like **Kubectl** . The request should be in a YAML format or JSON format.
29. **Deployment:** The deployment component defines how many pods need to be created, and the controller manager ensures that if the number of ***desired pods*** are not equal to the *actual pods*, then it automatically deploys another pod balancing the load this way.
30. Configuration: The configuration has a criteria that we need to follow when declaring the kubernetes configuration, example if its a *service* or *deployment*, then each will have its own ***attributes*** respectively, in the YAML file.
31. The Kubernetes Configuration has 3 components:
	a. Metadata
	b. Specification
	c. State (Desired State = Actual/Current State)
32. Kubernetes has a self healing mechanism, the status data comes from the ***etcd.*** It is the component that holds the current status of the pods and kubernetes cluster.

**Demo Application**

1. This project demonstrates a simple web application and its interaction with a database.
2. Database: Mongodb, *The web application will connect and interact with the database using an external configuration for DB URL and credentials.*
3. Requirements:
	a. Config map for the MongoDB endpoint
	b. Secret for MongoDB username + password
	c. Configuration file to deploy MongoDB + its Service
	d. Kubernetes Configuration file to deploy the Web App + its service
4. Storing the configuration files: The YAML file should be part of the application code, or you can have a separate Git repository where you can store all the YAML configuration files.
5. Architecture: Before you deploy your kubernetes cluster, you need to test it in your local machine, and you would require system and hardware resources to be able to test run the cluster, it could be a complex task. A solution for the is **Minikube.**
6. Minikube allows you to run a single node, that can run *master processes* and *worker processes* inside a single node. It also has a *Docker run time preinstalled in it.*
7. In order to create the services, you need to run the Kubernetes Utility Programs, and the way to do that is either *UI, APIS or a CLI called Kubectl.* The interaction with the Kubernetes Cluster is done through a client. And these 3 are different forms of client interaction, the most powerful being the CLI, Kubectl.
8. Kubectl allows you to interact with any type of Kubernetes cluster, whether is a *Hybrid architecture, Remote, Cloud, etc.*
9. For minikube documentaton [doc](https://minikube.sigs.k8s.io/docs/)
10. ***Kubectl*** gets installed as a dependency along with Minkube installation. 
11. Run *minikube start --driver docker*, after installing Docker + minikube. Run this command if you are running it for the first time. Otherwise just run *minikube start* on your CMD.
12. ***Comman Errors:*** Sometimes when you restart your Minikube cluster, it may give you an error like the following:
```
C:\Users\USER>minikube status
E0604 23:09:24.297517   11644 status.go:458] kubeconfig endpoint: got: 127.0.0.1:49410, want: 127.0.0.1:55612
minikube
type: Control Plane
host: Running
kubelet: Stopped
apiserver: Stopped
kubeconfig: Misconfigured


WARNING: Your kubectl is pointing to stale minikube-vm.
To fix the kubectl context, run `minikube update-context`

C:\Users\USER>minikube update-context
* "minikube" context has been updated to point to 127.0.0.1:55612
* Current context is "minikube"

HOW TO FIX THIS?

1. Run the following command: minikube update-context
```

12. **Minikube update-context *command:*** The `minikube update-context` command updates your `kubectl` configuration to point to the correct and current Minikube cluster endpoint. It fixes issues where `kubectl` talks to an old or wrong cluster address.
13. ***Minkube status:*** This command is used to check the kubernetes status, if you notice the *Kubelete & Api server* is stopped, then restart the minikube, below is an example:

```
C:\Users\USER>minikube status
minikube
type: Control Plane
host: Running
kubelet: Stopped
apiserver: Stopped
kubeconfig: Configured

HOW TO FIX THIS?

1. Run minikube start again.
2. Then check status: minikube status command. It should show the following:

C:\Users\USER>minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

14. Minikube is just for the startup, everything else is done and handled by the *kubectl* command line. Summary:
	a. To start the `kubelet` and `apiserver`, run:
```
minikube start

```
b. This will initialize and start all necessary components, including the kubelet and API server. If they're still not running after this, try:

```
minikube stop
minikube delete
minikube start

This would reset everything and fixes any bugs automatically.
```

15. To create a base-64 username + password do the following in your CMD:

```
EXAMPLE user + Password generation on Bash or Linux based Shell:

echo -n mongouser | base64
bW9asdas1c2Vy
echo -n mongopassword | base64
bW9uZsdfXNzd29yZA==

```

16. Deployment + Service for Mongodb: All deployments need their service, so its good practice to group them together in a single file. Example mongo.yaml
17. Important Commands:
	a. **kubectl get pods:** Lists down the pods that are currently running.
	b. **kubectl apply -f mongo-config.yaml**: This applies the mongo configuration file in kubernetes.
	c. **kubectl apply -f mongo-secret.yaml:** Create secret
	d. **kubectl apply -f mongo.yaml:** Creates the database configuration
	e. **kubectl apply -f webapp.yaml:** This helps to deploy our web application.
	f. **kubectl get all:** To check all of the deployments and pods statuses. *config map and secret won't appear in this list.*
	g. **kubectl get configmap**: To get config map details
	h. **kubectl get secrets:** To get the secrets details
	i. **kubectl --help**: To list documentation about kubectl.
	j. **kubectl get --help:** Gives all the available options.
	k. **kubectl get:** helps you to list down all the components that you will be using and their summary info.
	l. **kubectl describe pod <`instance of the service`>** : Example *kubectl describe pod*
	m. **kubectl logs <`specify the name of the pod`>**: This will help you ***troubleshoot, debug*** or monitor the current status of the running pods.
	n. **kubectl describe service webapp-service**: This will give you more details about the web app service.

EXAMPLE for kubectl describe service webapp-service:

```
kubectl describe service webapp-service

OUTPUT:

kubectl describe service/webapp-service
Name:                     webapp-service
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=webapp
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.101.214.3
IPs:                      10.101.214.3
Port:                     <unset>  3000/TCP
TargetPort:               3000/TCP
NodePort:                 <unset>  30100/TCP
Endpoints:                10.244.0.21:3000
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>
```

EXAMPLE for kubectl describe pod:
```
Example Command:
kubectl describe pod mongo-deployment-7cccf8b6d8-zrmbw                                  

OUTPUT:
Name:             mongo-deployment-7cccf8b6d8-zrmbw
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Sat, 29 Mar 2025 07:03:48 +0500
Labels:           app=mongo
                  pod-template-hash=7cccf8b6d8
Annotations:      <none>
Status:           Running
IP:               10.244.0.23
IPs:
  IP:           10.244.0.23
Controlled By:  ReplicaSet/mongo-deployment-7cccf8b6d8
Containers:
  mongodb:
    Container ID:   docker://08528d4be3bf2f26c40ea131b6f7de321c72c475f5368f3bb5d9447e04541fb0
    Image:          mongo:5.0
    Image ID:       docker-pullable://mongo@sha256:54bcd8da3ea5eec561b68c605046c55c6b304387dc4c2bf5b3a5f5064fbb7495
    Port:           27017/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Wed, 04 Jun 2025 23:14:42 +0500
    Last State:     Terminated
      Reason:       Error
      Exit Code:    255
      Started:      Sun, 30 Mar 2025 02:16:27 +0500
      Finished:     Wed, 04 Jun 2025 23:04:49 +0500
    Ready:          True
    Restart Count:  6
    Environment:
      MONGO_INITDB_ROOT_USERNAME:  <set to the key 'mongo-user' in secret 'mongo-secret'>      Optional: false
      MONGO_INITDB_ROOT_PASSWORD:  <set to the key 'mongo-password' in secret 'mongo-secret'>  Optional: false

```

EXAMPLE for kubectl logs

```
$ kubectl get pod

OUTPUT:
NAME                                 READY   STATUS    RESTARTS       AGE
mongo-deployment-7cccf8b6d8-zrmbw    1/1     Running   6 (132m ago)   67d
webapp-deployment-6bb4795f54-kdwq5   1/1     Running   6 (132m ago)   67d -> Example
-------------------------------
$ kubectl logs webapp-deployment-6bb4795f54-kdwq5

OUTPUT:
app listening on port 3000!
```

18. How do we access the web service from the browser? **kubectl get service**
```
kubectl get service
OUTPUT:

$ kubectl get service
NAME             TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
kubernetes       ClusterIP   10.96.0.1      <none>        443/TCP          67d
mongo-service    ClusterIP   10.109.65.17   <none>        27017/TCP        67d
webapp-service   NodePort    10.101.214.3   <none>        3000:30100/TCP   67d
```

19. We need the ip address of the minikube to access the web service through the browser: ***minikube ip*** or ***kubectl get node*** or ***kubectl get node -0 wide*** or ***kubectl get svc -o wide*** or ***kubectl get pod -o wide***

```
minikube ip

output:

http://192.168.49.2

```

20. Go to your browser and type the ip + :30100 -> `http://192.168.49.2:30100/`
21. If step 20 doesn't work, then probably your Windows is blocking the ip for the following reasons:
	a. Windows Defender Firewall
	b. Antivirus
	c. Minikube runs inside a VM or Docker container, so **network routing from your host to the NodePort can be blocked or not properly forwarded**.
	d. Unlike LoadBalancer with `minikube tunnel`, NodePort relies on direct access to Minikube’s network, which Windows sometimes restricts.

### Solution 1

1. Press the Windows Key + s
2. Search for 'Windows Defender Firewall' and open it.
3. Go to advanced settings
4. In the **Windows Defender Firewall with Advanced Security** window:
    a. Click **Inbound Rules** (left side)
    b. On the right, click **New Rule...**
        
5. **Create a rule:**
    a. **Rule Type:** Select **Port**, click **Next**
    b. **Protocol:** Select **TCP**
    c. **Specific local ports:** Enter `30100`, click **Next**
    d. **Allow the connection**, click **Next**
    e. Check all boxes (Domain, Private, Public), click **Next**
    f. Name it: `Minikube NodePort`, click **Finish**
        
6. Repeat the same for **Outbound Rules**, just in case.
7. If this solution doesn't work then sometimes Windows does not allow you to access Minikube ip.

### Solution 2

1. Run the following command on your terminal:
```
kubectl port-forward service/webapp-service 8080:3000

```
2. Use the following on your browser: `http://localhost:8080`
3. This should work.

### Solution 3

1. Open and edit your web-app.yaml file, by replacing the 'type:nodePort' with 'type: LoadBalancer'
```
spec:
  type: LoadBalancer
  selector:
```
2. Now run the following command to get the External IP

```
kubectl get svc webapp-service

OUTPUT:

NAME             TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
webapp-service   LoadBalancer   10.101.214.3   127.0.0.1     3000:30100/TCP   67d
```
3. Copy the external ip and run the following on your browser: `http://127.0.0.1`
4. This should work.
### Why NodePort Doesn’t Work:

1. **Minikube runs inside Docker or a VM**  
    → So the service is **not directly on your Windows system**, it's inside a virtual environment.
    
2. **NodePort exposes a port on the Minikube VM IP**  
    → Example: `192.168.49.2:30100`
    
3. **Windows firewall or antivirus may block this IP/port**  
    → Your browser can’t reach the Minikube VM from outside due to **blocked or untrusted local IP traffic**.
    
4. **Windows networking isn’t fully compatible**  
    → Unlike Linux, Windows doesn't easily allow routing to internal virtual IPs from the browser.

### What is the difference between LoadBalancer and nodePort?

1. **NodePort:** Opens a specific port (like 30100) on **each node’s IP**. You access the service by `<NodeIP>:<NodePort>`. Works well on real multi-node clusters or Linux setups, but can have network/firewall issues on local setups like Minikube on Windows.
2. **LoadBalancer:** Creates an external IP (via cloud provider or `minikube tunnel`) that **load balances traffic** to your service. Easier for local development with Minikube on Windows because the tunnel forwards traffic properly and bypasses firewall/network issues.