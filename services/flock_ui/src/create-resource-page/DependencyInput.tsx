import { UseFormRegister } from "react-hook-form";
import { BaseResourceSchema, ResourceFormData } from "../schemas";

interface Props {
  dependencyList: string[];
  dependencyMap: Map<string, BaseResourceSchema>;
  onClickChoose: (d: string) => void;
  register?: UseFormRegister<ResourceFormData>;
}

const DependencyInput = ({
  dependencyList,
  dependencyMap,
  onClickChoose,
}: Props) => {
  return (
    <>
      {dependencyList.map((dependency, index) => {
        const resource = dependencyMap.get(dependency);
        const name = resource?.metadata.name || "";
        const namespace = resource?.namespace || "";
        const kind = resource?.kind || "";

        return (
          <div key={index} className="form-control">
            <label className="form-label" htmlFor="dependencies">
              <strong>{dependency}</strong>
            </label>
            <div className="input-group mb-3">
              <button
                className="btn btn-outline-primary"
                type="button"
                id={`button-addon-${dependency}`}
                onClick={() => onClickChoose(dependency)}
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

export default DependencyInput;
