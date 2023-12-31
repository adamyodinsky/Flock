import yaml from "js-yaml";
import { useState } from "react";
import {
  Control,
  UseFormRegister,
  UseFormSetValue,
  useFieldArray,
} from "react-hook-form";
import Modal from "../components/Modal";
import { BaseResourceSchema, ResourceFormData } from "../schemas";
import { ResourceParams } from "../services/resourceService";
import ResourcesTable from "./ResourcesTable";

interface Tool {
  name: string;
  namespace: string;
  kind: string;
  id: string;
}

interface Props {
  register: UseFormRegister<ResourceFormData>;
  setValue: UseFormSetValue<ResourceFormData>;
  control: Control<ResourceFormData>;
}

const ToolsInput = ({ register, control }: Props) => {
  const [showTableModal, setShowTableModal] = useState(false);
  const [tableFilter, setTableFilter] = useState<ResourceParams>({});
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();

  const { fields, append, remove } = useFieldArray({
    control,
    name: "tools",
  });

  const handleCloseTableModal = () => {
    setShowTableModal(false);
  };

  const handleTableRawClick = (resource: BaseResourceSchema) => {
    setSelectedResource(resource);
    setShowResourceModal(true);
  };

  const handleCloseResourceModal = () => {
    setShowResourceModal(false);
  };

  const handleClickAdd = (filter: ResourceParams) => {
    setTableFilter(filter);
    setShowTableModal(true);
  };

  const handleOnSaveResourceModal = (e: BaseResourceSchema | undefined) => {
    if (!e) return;

    append({
      name: e.metadata.name,
      kind: e.kind,
      namespace: e.namespace,
    });

    setShowResourceModal(false);
    setShowTableModal(false);
  };

  return (
    <>
      <div className="m-1">
        <button
          className="btn btn-outline-primary"
          type="button"
          id="add-tool-button"
          onClick={() => handleClickAdd({ category: "tool" })}
        >
          Add Tool
        </button>
      </div>
      {fields.map((field, index) => {
        const name = field.name || "";
        const namespace = field.namespace || "";
        const kind = field.kind || "";

        return (
          <div key={index} className="form-control">
            <label className="form-label">
              <strong>{kind}</strong>
            </label>
            <div className="input-group m-1">
              <input
                {...register(`tools.${index}.kind`)}
                type="hidden"
                className="form-control"
                placeholder="Kind"
                aria-label="Kind"
                value={kind}
                readOnly
              />
              <input
                {...register(`tools.${index}.name`)}
                type="text"
                className="form-control"
                placeholder="Name"
                aria-label="Name"
                value={name}
                readOnly
              />
              <input
                {...register(`tools.${index}.namespace`)}
                type="text"
                className="form-control"
                placeholder="Namespace"
                aria-label="Namespace"
                value={namespace}
                readOnly
              />
              <button
                className="btn btn-outline-danger"
                type="button"
                id="add-tool-button"
                onClick={() => remove(index)}
              >
                Remove
              </button>
            </div>
          </div>
        );
      })}
      <Modal
        title="Resources"
        showModal={showTableModal}
        onClose={handleCloseTableModal}
        extraClassNames="modal-xl"
      >
        <ResourcesTable filter={tableFilter} onRawClick={handleTableRawClick} />
      </Modal>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={handleCloseResourceModal}
        showModal={showResourceModal}
        onSave={() => handleOnSaveResourceModal(selectedResource)}
        saveButtonText="Save Choice"
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </>
  );
};

export default ToolsInput;
