import Button from "../general-components/Button";
import { BaseResourceSchema } from "../schemas";

interface Props {
  onRawClick?: (e: BaseResourceSchema) => void;
  onDetails?: (e: BaseResourceSchema) => void;
  onDelete?: (e: BaseResourceSchema) => void;
  onEdit?: (e: BaseResourceSchema) => void;
  resourceList: BaseResourceSchema[];
  onDetailsText?: string;
  onEditText?: string;
  onDeleteText?: string;
}

const ResourcesTable = ({
  onRawClick,
  onDetails,
  onDelete,
  onEdit,
  resourceList,
  onDetailsText = "Details",
  onEditText = "Edit",
  onDeleteText = "Delete",
}: Props) => {
  return (
    <>
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
                <>
                  {onDetails && (
                    <td>
                      <Button
                        color="outline-primary"
                        onClick={() => onDetails(e)}
                      >
                        {onDetailsText}
                      </Button>
                    </td>
                  )}
                  {onEdit && (
                    <td>
                      <Button color="outline-warning" onClick={() => onEdit(e)}>
                        {onEditText}
                      </Button>
                    </td>
                  )}
                  {onDelete && (
                    <td>
                      <Button
                        color="outline-danger"
                        onClick={() => onDelete(e)}
                      >
                        {onDeleteText}
                      </Button>
                    </td>
                  )}
                </>
              }
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};

export default ResourcesTable;
