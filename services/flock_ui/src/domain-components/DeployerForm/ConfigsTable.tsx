import { ConfigResponseObj } from "../../deployments_schemas";
import Button from "../../general-components/Button";

interface Props {
  onRawClick?: (e: ConfigResponseObj) => void;
  onDetails?: (e: ConfigResponseObj) => void;
  onDelete?: (e: ConfigResponseObj) => void;
  onEdit?: (e: ConfigResponseObj) => void;
  configList: ConfigResponseObj[];
  onDetailsText?: string;
  onEditText?: string;
  onDeleteText?: string;
}

const ConfigsTable = ({
  onRawClick,
  onDetails,
  onDelete,
  onEdit,
  configList,
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
          {configList.map((e) => (
            <tr key={e.id} onClick={() => onRawClick && onRawClick(e)}>
              <td>{e.name}</td>
              <td>{e.kind}</td>
              <td>{e.description}</td>
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

export default ConfigsTable;
