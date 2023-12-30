import yaml from "js-yaml";
import { useEffect, useState } from "react";
import Modal from "../components/Modal";
import { BaseResourceSchema } from "../schemas";
import { ResourceParams, ResourceService } from "../services/resourceService";

interface Props {
  filter: ResourceParams;
  onRawClick: (e: BaseResourceSchema) => void;
  onClose: () => void;
  onSave?: (e: BaseResourceSchema) => void;
}

const ResourcesTable = ({ filter, onSave, onRawClick, onClose }: Props) => {
  const [resourceList, setResourceList] = useState<BaseResourceSchema[]>([]);
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);

  const apiService = new ResourceService();

  useEffect(() => {
    const { request, cancel } = apiService.getAll(filter);

    request
      .then((response) => {
        setResourceList(response.data.items);
        console.log(response.data);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.message);
      });

    return () => cancel();
  }, []);

  // const handleRowClick = (resource: BaseResourceSchema) => {
  //   setSelectedResource(resource);
  //   setShowModal(true);
  // };

  // const handleCloseModal = () => {
  //   setShowModal(false);
  //   setSelectedResource(undefined);
  // };

  return (
    <>
      <p className="text-danger">{error}</p>
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
            <tr key={e.id} onClick={() => onRawClick(e)}>
              <td>{e.metadata.name}</td>
              <td>{e.kind}</td>
              <td>{e.metadata.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={handleCloseModal}
        showModal={showModal}
        onSave={onSave}
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </>
  );
};

export default ResourcesTable;
