import { UseFormRegister } from "react-hook-form";
import { BaseResourceSchema, ResourceFormData } from "../schemas";

interface Props {
  toolsList: string[];
  toolsMap: Map<string, BaseResourceSchema>;
  onClickAdd: () => void;
  register?: UseFormRegister<ResourceFormData>;
}

const ToolsInput = ({ toolsList, toolsMap, onClickAdd }: Props) => {
  return (
    <>
      <button
        className="btn btn-outline-primary"
        type="button"
        id="add-tool-button"
        onClick={() => onClickAdd()}
      >
        Add Tool +
      </button>
      {toolsList.map((tool, index) => {
        const resource = toolsMap.get(tool);
        const name = resource?.metadata.name || "";
        const namespace = resource?.namespace || "";
        const kind = resource?.kind || "";

        return (
          <div key={index} className="form-control">
            <label className="form-label" htmlFor="tools">
              <strong>{tool}</strong>
            </label>
            <div className="input-group mb-3">
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
