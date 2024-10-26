# AWX/AAP Crednetial Plugin for Github Apps

Was tested on AWX 23.5.1, but *should* work for newer versions with the plugin archtecture as both entry points are specified in the build.

## Usage
With the continerized version of AWX doing installation of the external packages needs to be done at container build time. The best method of doing this is to wrap the task and web containers in your own Dockerfile and install this package.

For testing pruposes you can use minikube to install the package directly inside the container.

1. Get the pod names for both task and web
```shell
$ kubectl get pods

NAME                                               READY   STATUS    RESTARTS   AGE
awx-demo-postgres-13-0                             1/1     Running   0          6h1m
awx-demo-task-6d856db85-8ph5s                      4/4     Running   0          4h45m
awx-demo-web-94554596f-d87k4                       3/3     Running   0          4h45m
awx-operator-controller-manager-6c5879f7c5-jcblw   2/2     Running   0          4h45m
```

2. Get the container ID for the awx-demo-task (or whatever you named it) container
```shell
$ kubectl get pods awx-demo-task-6d856db85-8ph5s -o yaml

...
      readOnly: true
      recursiveReadOnly: Disabled
  - containerID: docker://0ba17fd042ef828c88573d20f19f4e51af85e913fe28afab1f04344a8142c7ea
    image: quay.io/ansible/awx:23.5.1
    imageID: docker-pullable://quay.io/ansible/awx@sha256:2d24fe9572852a1497c3c2514e6554cb4c6f01e9bfc775f5168ef53753f33248
    lastState: {}
    name: awx-demo-task
    ready: true
    restartCount: 0
...
```

3. Get the container ID for the awx-demo-web (or whatever you named it) container
```shell
$ kubectl get pods awx-demo-web-94554596f-d87k4 -o yaml

...
      readOnly: true
      recursiveReadOnly: Disabled
  - containerID: docker://cbfcb587d00f64498f069ce4fe3358af14d545dc07e73fe88c5b87293e477cee
    image: quay.io/ansible/awx:23.5.1
    imageID: docker-pullable://quay.io/ansible/awx@sha256:2d24fe9572852a1497c3c2514e6554cb4c6f01e9bfc775f5168ef53753f33248
    lastState: {}
    name: awx-demo-web
    ready: true
    restartCount: 0
...
```

4. SSH into the minikube box
```shell
$ minikube ssh
docker@minikube:~$ 
```

5. Log into task container as root with the container ID
```shell
docker@minikube:~$ docker exec -it -u0 0ba17fd042ef828c88573d20f19f4e51af85e913fe28afab1f04344a8142c7ea /bin/bash
bash-5.1# 
```

6. Install the credential plugin
```shell
bash-5.1# /var/lib/awx/venv/awx/bin/pip3 install -U awx-plugin-credential-github
...
```

7. Log into task container as root with the container ID
```shell
docker@minikube:~$ docker exec -it -u0 cbfcb587d00f64498f069ce4fe3358af14d545dc07e73fe88c5b87293e477cee /bin/bash
bash-5.1# 
```

8. Install the credential plugin
```shell
bash-5.1# /var/lib/awx/venv/awx/bin/pip3 install -U awx-plugin-credential-github
...
```

9. Update AWX
```shell
bash-5.1# awx-manage setup_managed_credential_types
```

10. Restart the task container
```shell
docker@minikube:~$ docker restart 0ba17fd042ef828c88573d20f19f4e51af85e913fe28afab1f04344a8142c7ea
```

11. Restart the web contianer
```shell
docker@minikube:~$ docker restart cbfcb587d00f64498f069ce4fe3358af14d545dc07e73fe88c5b87293e477cee
```

You should now be able to use the plugin in AWX.
