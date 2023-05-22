"""K8s deployer class"""

from flock_secrets_store import SecretStore

from flock_deployer.deployer.k8s.cron_job_deployer import K8sCronJobDeployer
from flock_deployer.deployer.k8s.deployment_deployer import K8sDeploymentDeployer
from flock_deployer.deployer.k8s.job_deployer import K8sJobDeployer
from flock_deployer.deployer.k8s.service_deployer import K8sServiceDeployer


class K8sDeployer:
    """K8s deployer class for deploying services and deployments

    Args:
        secret_store (SecretStore): Secret store

    Attributes:
        service_deployer (K8sServiceDeployer): Service deployer
        deployment_deployer (K8sDeploymentDeployer): Deployment deployer
    """

    def __init__(self, secret_store: SecretStore) -> None:
        """Initialize the deployer"""

        self.service_deployer = K8sServiceDeployer(secret_store)
        self.deployment_deployer = K8sDeploymentDeployer(secret_store)
        self.cron_job_deployer = K8sCronJobDeployer(secret_store)
        self.job_deployer = K8sJobDeployer(secret_store)
