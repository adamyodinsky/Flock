import { useEffect, useState } from "react";
import { BaseResourceSchema } from "../schemas";
import { ResourceParams, ResourceService } from "../services/services";
import Alert from "../components/Alert";

interface Props {
  filter: ResourceParams;
  onRawClick: (e: BaseResourceSchema) => void;
}

const ResourcesTable = ({ filter, onRawClick }: Props) => {
  const [resourceList, setResourceList] = useState<BaseResourceSchema[]>([]);
  const [error, setError] = useState([]);

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
