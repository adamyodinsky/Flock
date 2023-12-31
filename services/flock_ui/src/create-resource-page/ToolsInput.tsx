import { UseFormRegister } from "react-hook-form";
import { ResourceFormData } from "../schemas";
import { ResourceParams } from "../services/resourceService";

export interface Tool {
  name: string;
  namespace: string;
  kind: string;
}

interface Props {
  toolsList: Tool[];
  onClickAdd: () => void;
  onClickChoose: () => void;
  register?: UseFormRegister<ResourceFormData>;
}

const ToolsInput = ({ toolsList, onClickChoose }: Props) => {
  return (
    <>
      {toolsList.map((tool, index) => {
        const name = tool.name || "";
        const namespace = tool.namespace || "";
        const kind = tool.kind || "";

        return (
          <div key={index} className="form-control">
            <label className="form-label" htmlFor="dependencies">
              <strong>{`Tool ${index + 1}`}</strong>
            </label>
            <div className="input-group mb-3">
              <button
                className="btn btn-outline-primary"
                type="button"
                id={`button-addon-${tool}`}
                onClick={() => onClickChoose()}
              >
                Choose
              </button>
              <input
                type="text"
                className="form-control"
                placeholder="Kind"
                aria-label="Kind"
                value={kind}
                readOnly
              />
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                aria-label="Name"
                value={name}
                readOnly
              />
              <input
                type="text"
                className="form-control"
                placeholder="Namespace"
                aria-label="Namespace"
                value={namespace}
                readOnly
              />
            </div>
          </div>
        );
      })}
    </>
  );
};

export default ToolsInput;
