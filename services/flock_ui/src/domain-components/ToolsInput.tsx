import yaml from "js-yaml";
import { ReactNode, useState } from "react";
import {
  Control,
  UseFormRegister,
  UseFormSetValue,
  useFieldArray,
} from "react-hook-form";
import Alert from "../general-components/Alert";
import Button from "../general-components/Button";
import Modal from "../general-components/Modal";
import {
  BaseResourceSchema,
  BaseToolDependency,
  ResourceFormData,
} from "../resources_schemas";
import { ResourceParams, ResourceService } from "../services/resources_api";
import ResourcesTable from "./ResourcesTable";

interface Props {
  register: UseFormRegister<ResourceFormData>;
  setValue: UseFormSetValue<ResourceFormData>;
  control: Control<ResourceFormData>;
  initValue?: BaseToolDependency[];
}

const ToolsInput = ({ register, control }: Props) => {
  const [resourceTableList, setResourceTableList] = useState<
    BaseResourceSchema[]
  >([]);
  const [error, setError] = useState([]);
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [showTableModal, setShowTableModal] = useState(false);
  const [isTableLoading, setIsTableLoading] = useState(false);

  const { fields, append, remove } = useFieldArray({
    control,
    name: "tools",
  });

  const apiService = new ResourceService();

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
    setIsTableLoading(true);
    const { request } = apiService.getAll(filter);

    request
      .then((response) => {
        setResourceTableList(response.data.items);
        setError([]);
        setShowTableModal(true);
        setIsTableLoading(false);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.response.data.detail);
      });
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

  const getModalFooterButtons = (): ReactNode => {
    return (
      <>
        <Button
          type="button"
          color="outline-primary"
          onClick={() => handleOnSaveResourceModal(selectedResource)}
        >
          Save
        </Button>
      </>
    );
  };

  return (
    <>
      <Alert>
        {error.map((err) => (
          <pre>{err}</pre>
        ))}
      </Alert>
      <div className="m-1">
        <Button
          color="outline-primary"
          type="button"
          id="add-tool-button"
          onClick={() => handleClickAdd({ category: "tool" })}
        >
          {isTableLoading && (
            <span
              className="spinner-border spinner-border-sm me-2"
              aria-hidden="true"
            />
          )}
          Add Tool
        </Button>
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
                defaultValue={kind}
                readOnly
              />
              <input
                {...register(`tools.${index}.name`)}
                type="text"
                className="form-control"
                placeholder="Name"
                aria-label="Name"
                defaultValue={name}
                readOnly
              />
              <input
                {...register(`tools.${index}.namespace`)}
                type="text"
                className="form-control"
                placeholder="Namespace"
                aria-label="Namespace"
                defaultValue={namespace}
                readOnly
              />
              <Button
                color="outline-danger"
                type="button"
                id="add-tool-button"
                onClick={() => remove(index)}
              >
                Remove
              </Button>
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
        <ResourcesTable
          onRawClick={handleTableRawClick}
          resourceList={resourceTableList}
        />
      </Modal>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={handleCloseResourceModal}
        showModal={showResourceModal}
        footerButtons={getModalFooterButtons()}
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </>
  );
};

export default ToolsInput;
