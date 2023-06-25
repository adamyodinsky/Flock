import logging
import os

from kubernetes import client, config
from kubernetes.dynamic import DynamicClient


class K8sObserver:
    def __init__(self, default_label_selector: dict = {}) -> None:
        """Initialize the K8s Observer"""

        logging.debug("Initializing K8sCronJobDeployer")

        if os.environ.get("LOCAL", ""):
            config.load_kube_config()
            logging.debug("Using local kube config")
        else:
            config.load_incluster_config()
            logging.debug("Using in-cluster kube config")

        configuration = client.Configuration.get_default_copy()
        self.dyn_client = DynamicClient(client.ApiClient(configuration=configuration))

        if default_label_selector:
            self.default_label_selector = default_label_selector
        else:
            self.default_label_selector = {
                "label_selector": "flock=true",
            }

        self.metrics_v1beta1 = self.dyn_client.resources.get(
            api_version="metrics.k8s.io/v1beta1", kind="PodMetrics"
        )
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def _get_deployment_pod(self, deployment_name, namespace) -> object:
        """Get the pod for a deployment"""

        deployment = self.apps_v1.read_namespaced_deployment(deployment_name, namespace)

        label_selector = ",".join(
            [f"{k}={v}" for k, v in deployment.spec.selector.match_labels.items()]
        )

        pods = self.core_v1.list_namespaced_pod(
            namespace, label_selector=label_selector
        )

        return pods.items[0]

    def _get_parent_name_from_pod(self, pod_name) -> str:
        """Get the deployment name from a pod name"""

        result = pod_name.split("-")

        return "-".join(result[:-2])

    def _format_cpu(self, cpu: str) -> float:
        """Format the CPU value"""

        cpu = cpu.rstrip("n")
        cpu_in_cores = int(cpu) / (10**9)  # Convert from nano cores to cores
        return cpu_in_cores

    def _format_memory(self, memory: str) -> float:
        """Format the memory value"""

        memory = memory.rstrip("Ki")
        memory_in_mib = int(memory) / 1024  # Convert from KiB to MiB
        return memory_in_mib

    def get_metrics(self, namespace: str = "", label_selector: dict = {}) -> list[dict]:
        """Get metrics for all pods matching the label selector"""

        label_selector = {**self.default_label_selector, **label_selector}
        namespace_filter = {}

        if namespace:
            namespace_filter = {"namespace": namespace}

        logging.debug("Getting all pods metrics")

        metrics = self.metrics_v1beta1.get(**label_selector, **namespace_filter)

        result = []
        for pod_metrics in metrics.items:
            result.append(
                {
                    "name": self._get_parent_name_from_pod(pod_metrics.metadata.name),
                    "namespace": pod_metrics.metadata.namespace,
                    "cpu_usage": self._format_cpu(
                        pod_metrics.containers[0].usage["cpu"]
                    ),
                    "memory_usage": self._format_memory(
                        pod_metrics.containers[0].usage["memory"]
                    ),
                }
            )

        logging.debug(result)
        return result

    def get_single_metric(self, name, namespace, label_selector: dict = {}) -> dict:
        """Get metrics for a single pod"""

        label_selector = {**self.default_label_selector, **label_selector}

        logging.debug(f"Getting metrics for pod {name} in namespace {namespace}")
        pod_metrics = self.metrics_v1beta1.get(
            name=name, namespace=namespace, **label_selector
        )

        result = {
            "name": pod_metrics.metadata.name,
            "namespace": pod_metrics.metadata.namespace,
            "containers": [
                {
                    "name": container.name,
                    "cpu_usage": self._format_cpu(container.usage["cpu"]),
                    "memory_usage": self._format_memory(container.usage["memory"]),
                }
                for container in pod_metrics.containers
            ],
        }

        logging.debug(result)

        return result

    def details_for_all_namespaces(self) -> list[dict]:
        """Get details for all pods in all namespaces"""

        result = []
        response = self.core_v1.list_pod_for_all_namespaces(label_selector="flock=true")

        for i in response.items:
            result.append(
                {
                    "name": i.metadata.name,
                    "kind": i.metadata.owner_references[0].kind,
                    "phase": i.status.phase,
                    "namespace": i.metadata.namespace,
                    "ip": i.status.pod_ip,
                    "host_ip": i.status.host_ip,
                    "node_name": i.spec.node_name,
                }
            )

        logging.debug(result)

        return result

    # TODO: use the parent label selector, needs to think it over a little. maybe draw it
    def stream_logs(self, name, namespace):
        """Stream logs for a pod"""

        pod = self._get_deployment_pod(name, namespace)

        log = self.core_v1.read_namespaced_pod_log(
            name=pod.metadata.name,
            namespace=pod.metadata.namespace,
        )

        return log


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
