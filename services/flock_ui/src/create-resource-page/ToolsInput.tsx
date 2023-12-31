import { UseFormRegister } from "react-hook-form";
import { BaseResourceSchema, ResourceFormData } from "../schemas";

interface Props {
  toolsList: string[];
  toolsMap: Map<string, BaseResourceSchema>;
  onClickChoose: (d: string) => void;
  register?: UseFormRegister<ResourceFormData>;
}

const ToolsInput = ({ toolsList, toolsMap, onClickChoose }: Props) => {
  return (
    <>
      <button
        className="btn btn-outline-primary"
        type="button"
        id="button-add-tool"
      >
        +
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
              <button
                className="btn btn-outline-primary"
                type="button"
                id={`button-addon-${tool}`}
                onClick={() => onClickChoose(tool)}
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
