
### Project: Cloud-Ready IP Camera Recording with OpenCV, Docker, and Kubernetes

#### 1.0 Requirements

1. Docker
2. Minikube
3. Kubernetes
4. YAML Configuration file
5. DockerFile
6. Python script for IP Webcam
7. Requirements.txt file
8. **Python Libraries:** 
	a. opencv-python
	b. libgl1-mesa-glx \
	c. libglib2.0-0 \
9. Docker Hub account
10. WSL (If you are using Windows Operating System)
11. Project Docker image: https://hub.docker.com/repository/docker/sohaibsharih/mobile-cam-recorder/general

### 1.1 File Structure

```
Recording/
│
├── main.py
├── Dockerfile
├── recorder-deployment.yaml
├── README.md
└── requirements.txt   ← (for Python deps)
```

### 1.2 Dependencies

1. opencv-python
2. libgl1-mesa-glx \
3. libglib2.0-0 \
### 1.3 IP Smart Phone Webcam Python Script

Using **IP Webcam** (Streams over IP)
1. Install **IP Webcam** from Play Store.
2. Launch the app and start the server.
3. It will show an IP like `http://192.168.1.100:8080/video`.
4. Use the code below if you intend to run the script without Docker and Kubernetes

```
---main.py

import cv2

# Replace with your IP Webcam URL
url = "http://192.168.1.100:8080/video"
cap = cv2.VideoCapture(url)

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('mobile_camera_recording.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        cv2.imshow('Mobile Cam', frame)
        
        # Press 'q' to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to get frame.")
        break

cap.release()
out.release()
cv2.destroyAllWindows()

NOTES:

📂 Output

1. The script saves the video **directly to your laptop** as `mobile_camera_recording.avi`.
2. You can then import this raw file into any video editor.

```

5. Use the code below if you want to deploy it Kubernetes: *The reason why you need to do away with cv2.imshow is because Docker and Kubernetes do not need a Display environment to run the containerized applications, therefore it will return a **Qt error from OpenCV** since it's going to try to use GUI features (like `cv2.imshow`) — but Docker/Kubernetes environment **has no display server**. error, because a GUI interface is required. *

```
import cv2

# Replace with your IP Webcam URL

url = "http://192.168.100.39:8080/video"  # replace with your IP
cap = cv2.VideoCapture(url)

# Define VideoWriter
# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame.")
        break

    print("The video is recording... Success !!!")
    frame = cv2.resize(frame, (640, 480))  # optional resize
    out.write(frame)
    # cv2.imshow('frame', frame) #Commented because Kubernetes + Docker don't have GUI Features

     if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Below is Commented because Kubernetes + Docker don't have GUI Features
# cap.release()
# out.release()
# cv2.destroyAllWindows()
```


### 2.0 Step-by-Step guide for Containerization

1. Dockerfile

```
FROM python:3.10-slim

# Install system dependencies for OpenCV

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

  
# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY main.py .

#Run
CMD ["python", "main.py"]
```

2. Kubernetes Config file (YAML)

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mobile-cam-recorder

spec:
  replicas: 1
  selector:
    matchLabels:
      app: recorder
  template:
    metadata:
      labels:
        app: recorder
    spec:
      containers:
      - name: recorder
        image: sohaibsharih/mobile-cam-recorder
        imagePullPolicy: Always
        volumeMounts:
        - name: video-storage
          mountPath: /app

      volumes:
      - name: video-storage
        hostPath:
          path: /mnt/host-recordings
          type: Directory
```

3. Include a docker ignore file:
	a. Ignore all files and folders that don't need to be part of the docker build process.
	b. Examples: *venv folder, pycache, pyc,etc*

4. Include a requirements text file:
	a. Must include the dependencies that are needed to run the application.

5. Build and Tag the Docker Image

```
docker build -t exampleuserName/projectName .
```

6. Push the docker image

```
docker push username/projectname
```

7. If you have created a docker hub account, signup and register, then login.

```
docker login

NOTE: After the build process, once you've logged in then push your code. You need to login before pushing the image.
```

8. **Open CMD** and run the minikube server, *you should do this after you have started the **docker engine application.*** To start minikube:

```
minikube status --> Checks the current status

OUTPUT:

minikube
type: Control Plane
host: Stopped
kubelet: Stopped
apiserver: Stopped
kubeconfig: Stopped
------------------------------
minikube start ---> Starts minikube and will show you the running status.

OUTPUT:

* minikube v1.35.0 on Microsoft Windows 10 Pro 10.0.19045.5965 Build 19045.5965
* Using the docker driver based on existing profile
* Starting "minikube" primary control-plane node in "minikube" cluster
* Pulling base image v0.0.46 ...
* Restarting existing docker container for "minikube" ...
! Failing to connect to https://registry.k8s.io/ from both inside the minikube container and host machine
* To pull new external images, you may need to configure a proxy: https://minikube.sigs.k8s.io/docs/reference/networking/proxy/
* Preparing Kubernetes v1.32.0 on Docker 27.4.1 ...
* Verifying Kubernetes components...
  - Using image gcr.io/k8s-minikube/storage-provisioner:v5
* Enabled addons: default-storageclass, storage-provisioner
* kubectl not found. If you need it, try: 'minikube kubectl -- get pods -A'
* Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

9. **Additional Step (Optional): Check is Minikube Server is working by exploring the Minikube VM File System**. You can do this by running the following commands (example)

```
minikube ssh

Then use normal Linux commands like:

ls /mnt
ls -la /mnt/host-recordings

NOTES:
1. Once you are done, then you need to exit SSH, simply type 'exit' and enter.

```
10. **Create a Minikube Mount**
	a. Copy the Absolute path of the Directory where you would like to save the *output.avi* file at.
	b. Run the following Command:
```
minikube mount "E:\path\to\Recording:/mnt/host-recordings"

Expected OUTPUT:

* Mounting host path E:\MISCELLENEOUS\MY PROJECT\LEarning\Blockchain\Node js\My Assignments\Practice\Kubernetes\project_Two into VM as /mnt/host-recordings ...
  - Mount type:   9p
  - User ID:      docker
  - Group ID:     docker
  - Version:      9p2000.L
  - Message Size: 262144
  - Options:      map[]
  - Bind Address: 127.0.0.1:53715
* Userspace file server: ufs starting
* Successfully mounted E:\MISCELLENEOUS\MY PROJECT\LEarning\Blockchain\Node js\My Assignments\Practice\Kubernetes\project_Two to /mnt/host-recordings

* NOTE: This process must stay alive for the mount to be accessible ...

```
11. **How is `/mnt/host-recordings` created?** 
	a. It's created **automatically by `minikube mount`** when you run: `minikube mount "E:\...Recording:/mnt/host-recordings"`
	b. The name **`/mnt/host-recordings`** comes from **you** — it's the path you specify on the **right side** of the mount command.
12. **Create an Environment Variable for your Absolute Path(Optional)**: If your path is too long, you can store it inside an environment variable and then use that instead of the complete directory path on the ***minikube mount command.***.

```
Example

Open CMD
set RECORDING_PATH=E:\Your\Long\Project\Path\Recording

Check if it was created:

echo %RECORDING_PATH%

OUTPUT:
It should return the path you defined when creating the variable.

------------------------------
Now run the following command to mount

minikube mount "%RECORDING_PATH%:/mnt/host-recordings"

NOTE: Now leave your CMD opened and running. And run the deployment commands through your VS CODE Terminal
```
11. **Run and deploy** (VS Code Terminal Bash)

```
kubectl apply -f deployment-name.yaml
```

9. **Check if the deployment/pod is running:**

```
kubectl get pods
```

10. **Check if the script is running or the video is recording.**

```
kubectl logs -f <nameOfPod>

OUTPUT:
 print("The video is recording... Success !!!") --> Expected output. If this shows success then that means the camera is recording.

The video is recording... Success !!!
The video is recording... Success !!!
The video is recording... Success !!!
The video is recording... Success !!!
The video is recording... Success !!!
The video is recording... Success !!!
The video is recording... Success !!!
```

11. **Important Note and Pre-requisite:** 
	a. You'll have to turn on your **ip webcam** app on from your smart phone before you run the app.
	b. You'll see an IP address on the screen, take that and paste it in the python script in the ***URL variable.***
	c. Also ensure that both your computer/laptop and your smartphone are connected through the same Wifi connection in order for the application to work. The IP Webcam app streams over **local IP (e.g., `192.168.x.x`)**, which isn’t accessible over the internet unless you:
	- Set up **port forwarding** on your router (⚠️ security risk), or
	- Host the app on a **public IP or VPN** (advanced setup) 

12. **How to STOP recording?** *The camera would stop recording and generate an OUTPUT file once your **delete the pod using the following command:***

```
kubectl delete -f deployment-app.yaml

NOTE: It may take a few seconds or even a minute depending upon the duration of the recording, for the output avi file to be generated, and it will be saved in the Absolute Path you provided.
```
### 2.1 Strategy for saving your video(output) file

#### Method 1

1. **Pod:** The python script generates the output file and saves it inside the Pod, as long as the pod is running, it will stay there, the minute you delete the pod, it will get deleted. So its temporarily there. You can use the **kubectl cp** command to copy it to your current working directory. 

2. Where is the video being saved?
	a. When you run your app in Kubernetes: *The `.avi` file (in your case, `output.avi`) is saved **inside the container's file system**. This storage is **temporary** — when the pod is deleted, the file is **lost** unless saved elsewhere.*

3. **Saving the file to your local directory:** 
	a. **Copies the file** from inside the container **to your local machine**.
	b. It **does NOT delete** the original from the container.
	c. It behaves like a regular `cp` (copy) command.
	
```
USE THIS COMMMAND TO COPY:

kubectl cp <pod-name>:/app/output.avi ./output.avi
```

#### Method 2

1. **Volume Mount:** You can mount a volume and save the file in your local system by mapping the minikube server file location to your windows absolute path directory.
2. **VolumeMounts Flow**: Below Table shows how **Kubernetes `volumeMounts`** and `hostPath` work together, especially with **Minikube** and your **Windows (or Ubuntu) system**.


| YAML Property          | Example Value        | Purpose / What It Represents                                             |
| ---------------------- | -------------------- | ------------------------------------------------------------------------ |
| name                   | video-storage        | Identifier to connect `volumeMounts` to a `volume`                       |
| mountPath              | /app                 | Path **inside the container** where the host volume will be mounted      |
| `path` (in `hostPath`) | /mnt/host-recordings | Path **inside Minikube VM (host)** where data is actually stored         |
| type                   | Directory            | Declares that you're mounting a folder (directory), not a file or socket |

3. How It Works (on Windows + Minikube)
	a. You mounted your **Windows folder** to **Minikube’s Linux VM** like this: `minikube mount "%RECORDING_PATH%:/mnt/host-recordings"`
	b. - Inside the **Minikube VM**, `/mnt/host-recordings` now points to your **Windows folder**.
	c. In your YAML, you tell Kubernetes:
		- “Mount the host folder `/mnt/host-recordings`…”
		- “…into the container at `/app`”
	d. So anything your Python app writes to `/app/output.avi` (in the container) gets written **directly to your Windows folder**.
4. What happens if you run the application through a Linux Based OS like **Ubuntu** 
	a. Use an actual ***absolute path*** on your Linux system like:
```
path: /home/ahmed/Projects/Recording

```

**NOTE:** No `minikube mount` needed — because the path is already inside the Linux filesystem that Minikube can access natively.

5. **Current Flow through Windows Minikube:**

```
Your Python code writes to --> /app/output.avi (inside container)
Mapped via volumeMount --> to hostPath: /mnt/host-recordings (Minikube VM)
Mounted via minikube mount --> to Windows folder (e.g. E:\...Recording)

```

You end up writing **from container → to pod → to Minikube VM → to your Windows file system**.


### Common Errors

1. **Check the issue:** `kubectl logs mobile-cam-recorder-84fb8d967c-r26rc`
OUTPUT:

```
Traceback (most recent call last):
  File "/app/main.py", line 1, in <module>
    import cv2
  File "/usr/local/lib/python3.10/site-packages/cv2/__init__.py", line 181, in <module>
    bootstrap()
  File "/usr/local/lib/python3.10/site-packages/cv2/__init__.py", line 153, in bootstrap
    native_module = importlib.import_module("cv2")
  File "/usr/local/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```
5. **Fix the error:** 

```
OLD VERSION:

FROM python:3.10-slim

WORKDIR /app 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]

------------------

NEW VERSION:

FROM python:3.10-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]

```

### SOME COMMON ERRORS & DEBUGGING

```
Last Error:

kubectl logs mobile-cam-recorder-84fb8d967c-fxt7b
Traceback (most recent call last):
  File "/app/main.py", line 1, in <module>
    import cv2
  File "/usr/local/lib/python3.10/site-packages/cv2/__init__.py", line 181, in <module>
    bootstrap()
  File "/usr/local/lib/python3.10/site-packages/cv2/__init__.py", line 153, in bootstrap
    native_module = importlib.import_module("cv2")
  File "/usr/local/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
ImportError: libgthread-2.0.so.0: cannot open shared object file: No such file or directory

-------------------
check kubectl describe
kubectl describe pod mobile-cam-recorder-84fb8d967c-fxt7b
Name:             mobile-cam-recorder-84fb8d967c-fxt7b
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Sun, 22 Jun 2025 05:38:57 +0500
Labels:           app=recorder
                  pod-template-hash=84fb8d967c
Annotations:      <none>
Status:           Running
IP:               10.244.0.36
IPs:
  IP:           10.244.0.36
Controlled By:  ReplicaSet/mobile-cam-recorder-84fb8d967c
Containers:
  recorder:
    Container ID:   docker://eba2ee7481b1d1b059654e2fd26e2a90b35cd7c7cb46abb84b0cdba29d79ccdf
    Image:          sohaibsharih/mobile-cam-recorder
    Image ID:       docker-pullable://sohaibsharih/mobile-cam-recorder@sha256:6a761cf435d2b0532f687b56dc75f28049d662e5c8982437e58019b10a9469c5
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Sun, 22 Jun 2025 05:43:53 +0500
      Finished:     Sun, 22 Jun 2025 05:43:54 +0500
    Ready:          False
    Restart Count:  5
    Environment:    <none>
    Mounts:
      /app from video-storage (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-7889k (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       False
  ContainersReady             False
  PodScheduled                True
Volumes:
  video-storage:
    Type:          HostPath (bare host directory volume)
    Path:          /mnt/host-recordings
    HostPathType:  Directory
  kube-api-access-7889k:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                   From               Message
  ----     ------     ----                  ----               -------
  Normal   Scheduled  5m22s                 default-scheduler  Successfully assigned default/mobile-cam-recorder-84fb8d967c-fxt7b to minikube
  Normal   Pulled     3m49s                 kubelet            Successfully pulled image "sohaibsharih/mobile-cam-recorder" 
in 1m23.068s (1m23.068s including waiting). Image size: 591234705 bytes.
  Normal   Pulled     3m41s                 kubelet            Successfully pulled image "sohaibsharih/mobile-cam-recorder" 
in 2.742s (2.742s including waiting). Image size: 591234705 bytes.
  Normal   Pulled     3m22s                 kubelet            Successfully pulled image "sohaibsharih/mobile-cam-recorder" 
in 2.111s (2.111s including waiting). Image size: 591234705 bytes.
  Normal   Pulled     2m55s                 kubelet            Successfully pulled image "sohaibsharih/mobile-cam-recorder" 
in 2.045s (2.045s including waiting). Image size: 591234705 bytes.
  Normal   Pulled     2m4s                  kubelet            Successfully pulled image "sohaibsharih/mobile-cam-recorder" 
in 2.304s (2.304s including waiting). Image size: 591234705 bytes.
  Normal   Pulling    28s (x6 over 5m20s)   kubelet            Pulling image "sohaibsharih/mobile-cam-recorder"
  Normal   Created    26s (x6 over 3m47s)   kubelet            Created container: recorder
  Normal   Started    26s (x6 over 3m47s)   kubelet            Started container recorder
  Normal   Pulled     26s                   kubelet            Successfully pulled image "sohaibsharih/mobile-cam-recorder" 
in 2.194s (2.194s including waiting). Image size: 591234705 bytes.
  Warning  BackOff    10s (x15 over 3m39s)  kubelet            Back-off restartin
```

### Additional Notes

1. **Dockerfile Instructions:**

| Keyword | Meaning                                                          |
| ------- | ---------------------------------------------------------------- |
| FROM    | Sets the **base image** (e.g., Python)                           |
| RUN     | Runs commands **during image build**                             |
| WORKDIR | Sets the **working directory** inside the container              |
| COPY    | **Copies files** from your host into the image                   |
| CMD     | Defines the **default command** to run when the container starts |
2. Why 2 `RUN` Lines in the Dockerfile? Each RUN line:
	a. Executes a **shell command** inside the image during build.
	b. Creates a **new layer** in the Docker image.
	c. You can combine them, but it's often better to separate **system packages** (apt) from **Python packages** (pip) for clarity and caching.
3. ❌ `STATUS: ImagePullBackOff`: *This means **Kubernetes is unable to pull your Docker image** from Docker Hub.*
4. **Docker ignore file:** You can create a **.dockerignore** file and mention the files and folders you want to ignore to keep the image size small and efficient. Incase if you have uploaded the entire project directory by mistake, you can create a new build with the same name and push the image, it will overwrite the previous one, *rather than manually deleting the image from dockerhub.*

```
.dockerignore

venv/
__pycache__/
*.pyc
*.pyo

```

5. **Creating a Virtual Environment, incase if you want to run the python script without Docker + Kubernetes**Create a virtual Environment for your python project:
	a. **python -m venv venv**
	b. Activate the virtual environment
	c. Then install packages that are required. `Example: pip install opencv-python`
