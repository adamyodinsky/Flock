import yaml from "js-yaml";
import { ReactNode, useEffect, useState } from "react";
import { UseFormRegister, UseFormSetValue } from "react-hook-form";
import Button from "../general-components/Button";
import Modal from "../general-components/Modal";
import { BaseResourceSchema, ResourceFormData } from "../schemas";
import { ResourceParams, ResourceService } from "../services/services";
import ResourcesTable from "./ResourcesTable";

interface Props {
  dependencyKindList: string[];
  register: UseFormRegister<ResourceFormData>;
  setValue: UseFormSetValue<ResourceFormData>;
}

const apiService = new ResourceService();

const DependencyInput = ({ dependencyKindList, register, setValue }: Props) => {
  const [showTableModal, setShowTableModal] = useState(false);
  const [tableFilter, setTableFilter] = useState<ResourceParams>({});
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();
  const [dependencyMap, setDependencyMap] = useState<
    Map<string, BaseResourceSchema>
  >(new Map());
  const [error, setError] = useState([]);
  const [resourceList, setResourceList] = useState<BaseResourceSchema[]>([]);

  useEffect(() => {
    dependencyKindList.forEach((dependencyKind, index) => {
      const resource = dependencyMap.get(dependencyKind);
      if (resource) {
        setValue(`dependencies.${index}.kind`, resource.kind, {
          shouldValidate: true,
        });
        setValue(`dependencies.${index}.name`, resource.metadata.name, {
          shouldValidate: true,
        });
        setValue(`dependencies.${index}.namespace`, resource.namespace, {
          shouldValidate: true,
        });
      }
    });
  }, [dependencyMap]);

  useEffect(() => {
    const { request, cancel } = apiService.getAll(tableFilter);

    request
      .then((response) => {
        setResourceList(response.data.items);
        setError([]);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.response.data.detail);
      });

    return () => cancel();
  }, [tableFilter]);

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

  const handleClickChoose = (filter: ResourceParams) => {
    setTableFilter(filter);
    setShowTableModal(true);
  };

  const handleOnSaveResourceModal = (e: BaseResourceSchema | undefined) => {
    if (!e) return;

    const updatedDependencyMap = new Map(dependencyMap);
    updatedDependencyMap.set(e.kind, e);
    setDependencyMap(updatedDependencyMap);
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
      {dependencyKindList.map((dependencyKind, index) => {
        const resource = dependencyMap.get(dependencyKind);
        const name = resource?.metadata.name || "";
        const namespace = resource?.namespace || "";
        const kind = resource?.kind || "";

        return (
          <div key={index} className="form-control">
            <label className="form-label">
              <strong>{dependencyKind}</strong>
            </label>
            <div className="input-group m-1">
              <Button
                color="outline-primary"
                type="button"
                id={`button-addon-${dependencyKind}`}
                onClick={() => handleClickChoose({ kind: dependencyKind })}
              >
                Choose
              </Button>
              <input
                {...register(`dependencies.${index}.kind`)}
                type="hidden"
                className="form-control"
                placeholder="Kind"
                aria-label="Kind"
                defaultValue={kind}
                readOnly
              />
              <input
                {...register(`dependencies.${index}.name`)}
                type="text"
                className="form-control"
                placeholder="Name"
                aria-label="Name"
                defaultValue={name}
                readOnly
              />
              <input
                {...register(`dependencies.${index}.namespace`)}
                type="text"
                className="form-control"
                placeholder="Namespace"
                aria-label="Namespace"
                defaultValue={namespace}
                readOnly
              />
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
          resourceList={resourceList}
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

export default DependencyInput;
