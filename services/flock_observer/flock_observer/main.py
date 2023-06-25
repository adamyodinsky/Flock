import kubernetes
from kubernetes import client, config
from kubernetes.dynamic import DynamicClient


def list_deployment_pods(deployment_name, namespace):
    config.load_kube_config()

    # Create instances of the APIs
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    # Get the deployment
    deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)

    # Create a selector from the deployment's labels
    label_selector = ",".join(
        [f"{k}={v}" for k, v in deployment.spec.selector.match_labels.items()]
    )

    # Get the pods using the label selector
    pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)

    for pod in pods.items:
        print(f"Pod {pod.metadata.name} is managed by deployment {deployment_name}")


def get_deployment_pod(deployment_name, namespace):
    config.load_kube_config()

    # Create instances of the APIs
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    # Get the deployment
    deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)

    # Create a selector from the deployment's labels
    label_selector = ",".join(
        [f"{k}={v}" for k, v in deployment.spec.selector.match_labels.items()]
    )

    # Get the pods using the label selector
    pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)

    return pods.items[0]


def format_cpu(cpu):
    cpu = cpu.rstrip("n")
    cpu_in_cores = int(cpu) / (10**9)  # Convert from nano cores to cores
    return f"{cpu_in_cores} cores"


def format_memory(memory):
    memory = memory.rstrip("Ki")
    memory_in_mib = int(memory) / 1024  # Convert from KiB to MiB
    return f"{memory_in_mib} MiB"


######### this is the functions that should be exposed via the API ####


def get_pods_metrics():
    # Load the kube config settings
    config.load_kube_config()

    # Create a dynamic client
    configuration = client.Configuration.get_default_copy()

    dyn_client = DynamicClient(client.ApiClient(configuration=configuration))

    # Get the API resources for the metrics.k8s.io API
    v1beta1 = dyn_client.resources.get(
        api_version="metrics.k8s.io/v1beta1", kind="PodMetrics"
    )

    # Get a list of all the pod metrics
    all_pod_metrics = v1beta1.get(label_selector="flock=true")

    for pod_metrics in all_pod_metrics.items:
        print("Pod Name: ", pod_metrics.metadata.name)
        print("Namespace: ", pod_metrics.metadata.namespace)
        for container in pod_metrics.containers:
            print("Container Name: ", container.name)
            print("CPU Usage: ", format_cpu(container.usage["cpu"]))
            print("Memory Usage: ", format_memory(container.usage["memory"]))


def get_single_pod_metric(pod_name, namespace):
    # Load the kube config settings
    config.load_kube_config()

    # Create a dynamic client
    configuration = client.Configuration.get_default_copy()
    dyn_client = DynamicClient(client.ApiClient(configuration=configuration))

    # Get the API resources for the metrics.k8s.io API
    v1beta1 = dyn_client.resources.get(
        api_version="metrics.k8s.io/v1beta1", kind="PodMetrics"
    )

    # Get the metrics of the specified pod
    pod_metrics = v1beta1.get(name=pod_name, namespace=namespace)

    print("Pod Name: ", pod_metrics.metadata.name)
    print("Namespace: ", pod_metrics.metadata.namespace)
    for container in pod_metrics.containers:
        print("Container Name: ", container.name)
        print("CPU Usage: ", format_cpu(container.usage["cpu"]))
        print("Memory Usage: ", format_memory(container.usage["memory"]))


# Get all pods with label flock=true
def pod_details_for_all_namespaces():
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(label_selector="flock=true")
    for i in ret.items:
        print(
            i.metadata.owner_references[0].name,
            i.metadata.owner_references[0].kind,
            i.status.phase,
            i.metadata.namespace,
            i.status.pod_ip,
            i.spec.node_name,
            i.status.host_ip,
        )


# Stream logs from a single pod
def stream_pod_logs(name, namespace):
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()

    pod = get_deployment_pod(name, namespace)

    print(
        v1.read_namespaced_pod_log(
            name=pod.metadata.name,
            namespace=pod.metadata.namespace,
        )
    )


# /metrics/{namespace}/{name}
# /metrics/{namespace}
# get_pods_metrics()
# get_single_pod_metric(name, namespace)


# deployment/{namespace}/{name}
# deployment/{namespace}
# get_pods()
# get_deployment_pod("my-agent", "default")


# logs/{namespace}/{name}
# stream_pod_logs("my-agent", "default")
