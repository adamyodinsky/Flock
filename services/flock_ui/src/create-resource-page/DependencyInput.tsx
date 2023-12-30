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
  return (
    <>
      {dependencyList.map((dependency, index) => {
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
                onClick={() => onClickChoose()}
              >
                Choose {dependency}
              </button>
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                aria-label="Name"
                aria-describedby={`Name-${dependency}`}
                value={dependencyMap.get(dependency)?.metadata.name}
              />
              <input
                type="text"
                className="form-control"
                placeholder="Namespace"
                aria-label="Namespace"
                aria-describedby={`Namespace-${dependency}`}
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
