import { UseFormRegister } from "react-hook-form";
import { BaseResourceSchema, ResourceFormData } from "../schemas";
import { ResourceParams } from "../services/resourceService";

interface Props {
  dependencyKindList: string[];
  dependencyMap: Map<string, BaseResourceSchema>;
  onClickChoose: (filter: ResourceParams) => void;
  register?: UseFormRegister<ResourceFormData>;
}

const DependencyInput = ({
  dependencyKindList,
  dependencyMap,
  onClickChoose,
}: Props) => {
  return (
    <>
      {dependencyKindList.map((dependencyKind, index) => {
        const resource = dependencyMap.get(dependencyKind);
        const name = resource?.metadata.name || "";
        const namespace = resource?.namespace || "";
        const kind = resource?.kind || "";

        return (
          <div key={index} className="form-control">
            <label className="form-label" htmlFor="dependencies">
              <strong>{dependencyKind}</strong>
            </label>
            <div className="input-group mb-3">
              <button
                className="btn btn-outline-primary"
                type="button"
                id={`button-addon-${dependencyKind}`}
                onClick={() => onClickChoose({ kind: dependencyKind })}
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
