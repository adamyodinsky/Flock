import os

import pytest

from flock_observer.observer import K8sObserver

TEST_LABEL = "flock=true"


@pytest.fixture(scope="module")
def k8s_observer():
    # Make sure to set up your environment correctly, either locally or in-cluster.
    os.environ["LOCAL"] = "1"
    return K8sObserver(default_label_selector=TEST_LABEL)


def label_selector_test(label_selector: dict):
    observer = K8sObserver(default_label_selector=TEST_LABEL)

    metrics = observer.metrics(**label_selector)
    assert metrics

    details = observer.details(**label_selector)
    assert details

    logs = observer.logs(**label_selector)
    assert logs


def test_k8s_observer():
    # Here we assume that there is a deployment named 'x' in the 'y' namespace
    os.environ["LOCAL"] = "1"

    deployment_name = "my-agent"
    deployment_namespace = "default"
    deployment_kind = "FlockDeployment"

    # /{kind}/{namespace}/{name}
    label_selector_test(
        {
            "kind": deployment_kind,
            "namespace": deployment_namespace,
            "name": deployment_name,
        }
    )

    # /{kind}/{namespace}
    label_selector_test(
        {
            "kind": deployment_kind,
            "namespace": deployment_namespace,
        }
    )

    # /{kind}
    label_selector_test(
        {
            "kind": deployment_kind,
        }
    )

    # /{namespace}
    label_selector_test(
        {
            "namespace": deployment_namespace,
        }
    )

    # /
    label_selector_test({})


if __name__ == "__main__":
    pytest.main()
