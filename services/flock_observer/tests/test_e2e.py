import os

import pytest

from flock_observer.observer import K8sObserver

TEST_LABEL = {
    "label_selector": "flock=true",
}


@pytest.fixture(scope="module")
def k8s_observer():
    # Make sure to set up your environment correctly, either locally or in-cluster.
    os.environ["LOCAL"] = "1"
    return K8sObserver(default_label_selector=TEST_LABEL)


def test_k8s_observer(k8s_observer):
    # Here we assume that there is a deployment named 'test-deployment' in the 'test' namespace
    deployment_name = "my-agent"
    namespace = "default"

    # Get the pod for a deployment
    pod = k8s_observer._get_deployment_pod(deployment_name, namespace)
    assert pod

    # Get metrics for all pods matching the label selector
    metrics = k8s_observer.get_metrics(namespace=namespace)
    assert metrics

    # Get metrics for a single pod
    single_metric = k8s_observer.get_single_metric(pod.metadata.name, namespace)
    assert single_metric

    # Get details for all pods in all namespaces
    details = k8s_observer.details_for_all_namespaces()
    assert details

    # Stream logs for a pod
    logs = k8s_observer.stream_logs(pod.metadata.name, namespace)
    assert logs


if __name__ == "__main__":
    pytest.main()
