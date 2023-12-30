import { useEffect } from "react";
import { BaseResourceSchema } from "../schemas";

interface Props {
  dependencyList: string[];
  dependencyMap: Map<string, BaseResourceSchema>;
  onClickChoose: () => void;
}

const DependencyInput = ({
  dependencyList,
  dependencyMap,
  onClickChoose,
}: Props) => {
  useEffect(() => {
    console.log(dependencyList);
  }, [dependencyList]);

  return (
    <>
      {dependencyList.map((dependency) => {
        return (
          <div className="form-control">
            <label className="form-label" htmlFor="dependencies">
              <strong>{dependency}</strong>
            </label>
            <div className="input-group mb-3">
              <button
                className="btn btn-outline-primary"
                type="button"
                id="button-addon1"
                onClick={() => onClickChoose()}
              >
                Choose {dependency}
              </button>
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                aria-label="Name"
                aria-describedby="Name"
                value={dependencyMap.get(dependency)?.metadata.name}
              />
              <input
                type="text"
                className="form-control"
                placeholder="Namespace"
                aria-label="Namespace"
                aria-describedby="Namespace"
                value={dependencyMap.get(dependency)?.namespace}
              />
            </div>
          </div>
        );
      })}
    </>
  );
};

export default DependencyInput;
