import yaml from "js-yaml";
import { ReactNode, useEffect, useState } from "react";
import Alert from "../general-components/Alert";
import Button from "../general-components/Button";
import Modal from "../general-components/Modal";
import { BaseResourceSchema } from "../schemas";
import { ResourceService } from "../services/services";
import EditResourceForm from "./EditResourceForm/EditResourceForm";
import ResourcesTable from "./ResourcesTable";

const apiService = new ResourceService();

const ResourcesTablePage = () => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editResource, setEditResource] = useState<BaseResourceSchema>();
  const [deleteResource, setDeleteResource] = useState<BaseResourceSchema>();
  const [detailsResource, setDetailsResource] = useState<BaseResourceSchema>();
  const [showResourceModal, setShowDetailsModal] = useState(false);
  const [filter, setFilter] = useState({});
  const [resourceList, setResourceList] = useState<BaseResourceSchema[]>([]);
  const [error, setError] = useState([]);

  useEffect(() => {
    const { request, cancel } = apiService.getAll(filter);

    request
      .then((response) => {
        setResourceList(response.data.items);
        setError([]);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.response.data.detail);
      });

    return () => cancel();
  }, [filter]);

  const handleEditClick = (resource: BaseResourceSchema) => {
    setEditResource(resource);
    setShowEditModal(true);
  };

  const handleDeleteClick = (resource: BaseResourceSchema) => {
    setDeleteResource(resource);
    setShowDeleteModal(true);
  };

  const handleDetailsClick = (resource: BaseResourceSchema) => {
    setDetailsResource(resource);
    setShowDetailsModal(true);
  };

  const handleDeleteConfirmed = () => {
    const id = deleteResource?.id || "";

    apiService
      .delete(id)
      .then(() => {
        setResourceList(resourceList.filter((e) => e.id !== id));
        setError([]);
      })
      .catch((err) => {
        setError(err.response.data.detail);
      });

    setShowDeleteModal(false);
    setDeleteResource(undefined);
  };

  const getModalDeletionFooterButtons = (): ReactNode => {
    return (
      <>
        <Button color="outline-danger" onClick={() => handleDeleteConfirmed()}>
          Confirm Deletion
        </Button>
      </>
    );
  };

  return (
    <>
      <Alert>
        {error.map((err) => (
          <pre>{err}</pre>
        ))}
      </Alert>
      <ResourcesTable
        onDelete={handleDeleteClick}
        onDetails={handleDetailsClick}
        onEdit={handleEditClick}
        resourceList={resourceList}
      />
      <Modal
        title="Delete Resource"
        showModal={showDeleteModal}
        onClose={() => {
          setShowDeleteModal(false);
        }}
        footerButtons={getModalDeletionFooterButtons()}
      >
        <div>
          <p>
            {deleteResource?.metadata.name} {deleteResource?.kind} from{" "}
            {deleteResource?.namespace} namespace will be deleted.
          </p>
          <p>
            <strong>Are you sure you want to delete this resource?</strong>
          </p>
        </div>
      </Modal>
      <Modal
        title={`${editResource?.kind} ${editResource?.metadata.name}`}
        showModal={showEditModal}
        onClose={() => setShowEditModal(false)}
      >
        {editResource && <EditResourceForm resourceToEdit={editResource} />}
      </Modal>
      <Modal
        title={detailsResource?.metadata.name}
        onClose={() => setShowDetailsModal(false)}
        showModal={showResourceModal}
      >
        <pre>{yaml.dump(detailsResource)}</pre>
      </Modal>
    </>
  );
};

export default ResourcesTablePage;
