import logging
import os

from kubernetes import client, config
from kubernetes.dynamic import DynamicClient

from flock_observer.observer.base import DetailsModel, LogsModel, MetricsModel, Observer


class K8sObserver(Observer):
    def __init__(self, default_label_selector: str = "flock=true") -> None:
        """Initialize the K8s Observer"""

        logging.debug("Initializing K8sCronJobDeployer")

        if os.environ.get("LOCAL", ""):
            config.load_kube_config()
            logging.debug("Using local kube config")
        else:
            config.load_incluster_config()
            logging.debug("Using in-cluster kube config")

        configuration = client.Configuration.get_default_copy()
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.dyn_client = DynamicClient(client.ApiClient(configuration=configuration))

        self.metrics_v1beta1 = self.dyn_client.resources.get(
            api_version="metrics.k8s.io/v1beta1", kind="PodMetrics"
        )

        self.default_label_selector = default_label_selector

        if self.health_check():
            logging.info("K8s Observer initialized successfully")
        else:
            raise Exception("K8s Observer failed to initialize")

    def health_check(self) -> bool:
        """Health check

        Check the health of the deployer.

        Returns:
            bool: True if healthy
        """

        logging.info("Checking health")

        try:
            self.core_v1.list_pod_for_all_namespaces()
        except Exception:
            logging.exception("Health check failed")
            return False

        return True

    def _labels_selector_filter(
        self, kind: str = "", namespace: str = "", name: str = ""
    ) -> dict:
        label_selector = ""

        if kind:
            label_selector += f"parent_kind={kind},"
        if namespace:
            label_selector += f"parent_namespace={namespace},"
        if name:
            label_selector += f"parent_name={name},"

        label_selector += self.default_label_selector
        return {"label_selector": label_selector}

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

    def metrics(
        self, kind: str = "", namespace: str = "", name: str = ""
    ) -> list[MetricsModel]:
        """
        Get metrics by a filter name, namespace and kind

        Args:
            kind (str, optional): The kind of the parent object. Defaults to "".
            namespace (str, optional): The namespace of the parent object. Defaults to "".
            name (str, optional): The name of the parent object. Defaults to "".

        Returns:
            dict: A dict of metrics for the parent object
        """

        label_selector = self._labels_selector_filter(
            kind=kind, namespace=namespace, name=name
        )

        logging.debug("Getting all pods metrics")

        metrics = self.metrics_v1beta1.get(**label_selector)

        result = []
        for pod in metrics.items:
            result.append(
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "cpu_usage": self._format_cpu(pod.containers[0].usage["cpu"]),
                    "memory_usage": self._format_memory(
                        pod.containers[0].usage["memory"]
                    ),
                }
            )

        logging.debug(result)
        return result

    def details(
        self, kind: str = "", namespace: str = "", name: str = ""
    ) -> list[DetailsModel]:
        """Get details for all pods in all namespaces.

        Returns:
            list[dict]: A list of details for all pods in all namespaces.
        """

        label_selector = self._labels_selector_filter(
            kind=kind, namespace=namespace, name=name
        )

        response = self.core_v1.list_pod_for_all_namespaces(**label_selector)

        result = []
        for pod in response.items:
            result.append(
                {
                    "name": pod.metadata.name,
                    "kind": pod.metadata.owner_references[0].kind,
                    "phase": pod.status.phase,
                    "namespace": pod.metadata.namespace,
                    "ip": pod.status.pod_ip,
                    "host_ip": pod.status.host_ip,
                    "node_name": pod.spec.node_name,
                }
            )

        logging.debug(result)

        return result

    def logs(
        self, kind: str = "", namespace: str = "", name: str = ""
    ) -> list[LogsModel]:
        """Get logs for a pod

        Args:
            kind (str, optional): The kind of the parent object. Defaults to "".
            namespace (str, optional): The namespace of the parent object. Defaults to "".
            name (str, optional): The name of the parent object. Defaults to "".


        """

        label_selector = self._labels_selector_filter(
            kind=kind, namespace=namespace, name=name
        )

        response = self.core_v1.list_pod_for_all_namespaces(**label_selector)

        result = []
        for pod in response.items:
            logs = self.core_v1.read_namespaced_pod_log(
                namespace=pod.metadata.namespace, name=pod.metadata.name
            )
            result.append({"name": pod.metadata.name, "logs": logs})

        return result
