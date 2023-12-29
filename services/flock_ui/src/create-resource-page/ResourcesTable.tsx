import { useEffect, useState } from "react";
import Modal from "../components/Modal";
import { BaseResourceSchema } from "../schemas";
import { ResourceService } from "../services/resourceService";

const ResourcesTable = () => {
  const [resourceList, setResourceList] = useState<BaseResourceSchema[]>([]);
  const [error, setError] = useState("");
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();

  const apiService = new ResourceService();

  useEffect(() => {
    const { request, cancel } = apiService.getAll();

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

  useEffect(() => {
    console.log(resourceList);
  }, [resourceList]);

  const handleRowClick = (resource: BaseResourceSchema) => {
    setSelectedResource(resource);
  };

  const handleCloseModal = () => {
    setSelectedResource(undefined);
  };

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
            <tr key={e.id} onClick={() => handleRowClick(e)}>
              <td>{e.metadata.name}</td>
              <td>{e.kind}</td>
              <td>{e.metadata.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <Modal resource={selectedResource} onClose={handleCloseModal} />
    </>
  );
};

export default ResourcesTable;
