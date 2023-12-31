import { useEffect, useState } from "react";
import { BaseResourceSchema } from "../schemas";
import { ResourceParams, ResourceService } from "../services/resourceService";

interface Props {
  filter: ResourceParams;
  onRawClick: (e: BaseResourceSchema) => void;
}

const ResourcesTable = ({ filter, onRawClick }: Props) => {
  const [resourceList, setResourceList] = useState<BaseResourceSchema[]>([]);
  const [error, setError] = useState("");

  const apiService = new ResourceService();

  useEffect(() => {
    const { request, cancel } = apiService.getAll(filter);

    request
      .then((response) => {
        setResourceList(response.data.items);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.message);
      });

    return () => cancel();
  }, []);

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
    </>
  );
};

export default ResourcesTable;
