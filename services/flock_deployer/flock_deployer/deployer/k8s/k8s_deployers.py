"""K8s deployer class"""

from flock_common.secret_store import SecretStore
from flock_resource_store.base import ResourceStore

from flock_deployer.deployer.base import BaseDeployers
from flock_deployer.deployer.k8s.cron_job_deployer import K8sCronJobDeployer
from flock_deployer.deployer.k8s.deployment_deployer import K8sDeploymentDeployer
from flock_deployer.deployer.k8s.job_deployer import K8sJobDeployer
from flock_deployer.deployer.k8s.service_deployer import K8sServiceDeployer


class K8sDeployers(BaseDeployers):
    """K8s deployer class for deploying services and deployments

    Args:
        secret_store (SecretStore): Secret store

    Attributes:
        service_deployer (K8sServiceDeployer): Service deployer
        deployment_deployer (K8sDeploymentDeployer): Deployment deployer
    """

    def __init__(
        self,
        resource_store: ResourceStore,
        secret_store: SecretStore,
    ) -> None:
        """Initialize the deployer"""

        super().__init__(resource_store, secret_store)
        self.service_deployer = K8sServiceDeployer()
        self.deployment_deployer = K8sDeploymentDeployer()
        self.cron_job_deployer = K8sCronJobDeployer()
        self.job_deployer = K8sJobDeployer()
