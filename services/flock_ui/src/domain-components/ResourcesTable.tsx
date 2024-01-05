import { ReactNode, useEffect, useState } from "react";
import Alert from "../general-components/Alert";
import Button from "../general-components/Button";
import Modal from "../general-components/Modal";
import { BaseResourceSchema } from "../schemas";
import { ResourceParams, ResourceService } from "../services/services";

interface Props {
  filter: ResourceParams;
  onRawClick?: (e: BaseResourceSchema) => void;
  onDelete?: (e: BaseResourceSchema) => void;
  onEdit?: (e: BaseResourceSchema) => void;
}

const ResourcesTable = ({ filter, onRawClick }: Props) => {
  const [resourceList, setResourceList] = useState<BaseResourceSchema[]>([]);
  const [error, setError] = useState([]);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteResource, setDeleteResource] = useState<BaseResourceSchema>();

  const apiService = new ResourceService();

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
  }, []);

  const handleDeleteClick = (resource: BaseResourceSchema) => {
    setDeleteResource(resource);
    setShowDeleteModal(true);
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

  const getModalFooterButtons = (): ReactNode => {
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
      <table className="table table-bordered table table-hover">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Kind</th>
            <th scope="col">Description</th>
          </tr>
        </thead>
        <tbody>
          {resourceList.map((e) => (
            <tr key={e.id} onClick={() => onRawClick && onRawClick(e)}>
              <td>{e.metadata.name}</td>
              <td>{e.kind}</td>
              <td>{e.metadata.description}</td>
              {
                <td>
                  <Button
                    color="outline-danger"
                    onClick={() => handleDeleteClick(e)}
                  >
                    Delete
                  </Button>
                </td>
              }
            </tr>
          ))}
        </tbody>
      </table>
      <Modal
        title="Delete Resource"
        showModal={showDeleteModal}
        onClose={() => {
          setShowDeleteModal(false);
        }}
        footerButtons={getModalFooterButtons()}
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
    </>
  );
};

export default ResourcesTable;
