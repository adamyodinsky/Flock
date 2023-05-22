import abc

from flock_schemas.deployment import DeploymentSchema
from flock_schemas.job import CronJobSchema, JobSchema


class BaseManifestCreator(metaclass=abc.ABCMeta):
    """Abstract class for a manifest creator"""

    # @abc.abstractmethod
    # def create(self, name, namespace, target):
    #     """Create manifest"""

    # @abc.abstractmethod
    # def update(self, deployment: , dry_run=None):
    #     """Update manifest"""

    # @abc.abstractmethod
    # def delete(self, deployment: DeploymentSchema, dry_run=None):
    #     """Delete manifest"""
