import { zodResolver } from "@hookform/resolvers/zod";
import yaml from "js-yaml";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import Modal from "../components/Modal";
import {
  BaseResourceSchema,
  Kind,
  ResourceFormData,
  kindValues,
  resourceFormSchema,
} from "../schemas";
import { ResourceSchemaService } from "../services/resourceService";
import DependencyInput from "./DependencyInput";
import ResourcesTable from "./ResourcesTable";

interface Props {
  onSubmit: (data: ResourceFormData) => void;
}

const CreateResourceForm = (props: Props) => {
  const [kind, setKind] = useState<string>(Kind.Embedding);
  const [vendorList, setVendorList] = useState<string[]>([]);
  const [showTableModal, setShowTableModal] = useState(false);
  const [showResourceModal, setShowResourceModal] = useState(false);

  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();

  const [dependencyKind, setDependencyKind] = useState<string>();
  const [dependencyList, setDependencyList] = useState<string[]>([]);
  const [dependencyMap, setDependencyMap] = useState<
    Map<string, BaseResourceSchema>
  >(new Map());

  useEffect(() => {
    const service = new ResourceSchemaService();
    service.get(kind).then((response) => {
      setVendorList(response.data.vendor);
      setDependencyList(response.data.dependencies);
    });
  }, [kind]);

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<ResourceFormData>({ resolver: zodResolver(resourceFormSchema) });

  const onSubmitHandler = (data: ResourceFormData) => {
    props.onSubmit(data);
  };

  const handleTableRawClick = (resource: BaseResourceSchema) => {
    setSelectedResource(resource);
    setShowResourceModal(true);
  };

  const handleCloseTableModal = () => {
    setShowTableModal(false);
  };

  const handleClickChoose = (d: string) => {
    setDependencyKind(d);
    setShowTableModal(true);
  };

  const handleCloseResourceModal = () => {
    setShowResourceModal(false);
  };

  const handleOnSaveResourceModal = (e: BaseResourceSchema | undefined) => {
    if (!e) return;

    const updatedDependencyMap = new Map(dependencyMap);
    updatedDependencyMap.set(e.kind, e);
    setDependencyMap(updatedDependencyMap);
    setShowResourceModal(false);
    setShowTableModal(false);
  };

  return (
    <>
      <form className="form-control">
        <div className="mb-3">
          <label className="form-label" htmlFor="name">
            <strong>Name</strong>
          </label>
          <input
            {...register("name")}
            id="name"
            type="text"
            className="form-control"
          ></input>
          {errors.name && <p className="text-danger">{errors.name.message}</p>}
        </div>
        <div className="mb-3">
          <label htmlFor="description">
            <strong>Description</strong>
          </label>
          <input
            {...register("description")}
            id="description"
            type="text"
            className="form-control"
          ></input>
          {errors.description && (
            <p className="text-danger">{errors.description.message}</p>
          )}
        </div>
        <div className="mb-3">
          <label className="form-label" htmlFor="namespace">
            <strong>Namespace</strong>
          </label>
          <select
            {...register("namespace")}
            id="namespace"
            className="form-select"
          >
            <option value="default">default</option>
          </select>
          {errors.namespace && (
            <p className="text-danger">{errors.namespace.message}</p>
          )}
        </div>
        <div className="mb-3">
          <label className="form-label" htmlFor="kind">
            <strong>Kind</strong>
          </label>
          <select
            {...register("kind")}
            id="kind"
            className="form-select"
            onChange={(event) => setKind(event.target.value)}
          >
            {kindValues.map((val) => (
              <option key={val} value={val}>
                {val}
              </option>
            ))}
          </select>
          {errors.kind && <p className="text-danger">{errors.kind.message}</p>}
        </div>
        <div className="mb-3">
          <label className="form-label" htmlFor="vendor">
            <strong>Vendor</strong>
          </label>
          <select {...register("vendor")} id="vendor" className="form-select">
            {vendorList.map((val) => (
              <option key={val} value={val}>
                {val}
              </option>
            ))}
          </select>
          {errors.vendor && (
            <p className="text-danger">{errors.vendor.message}</p>
          )}
        </div>
        <div className="mb-3">
          <label className="form-label" htmlFor="dependencies">
            <strong>Dependencies</strong>
          </label>
          <DependencyInput
            onClickChoose={handleClickChoose}
            dependencyList={dependencyList}
            dependencyMap={dependencyMap}
          />
          {errors.dependencies && (
            <p className="text-danger">{errors.dependencies.message}</p>
          )}
        </div>
        <button
          disabled={!isValid}
          onClick={handleSubmit((data) => {
            console.log(data);
          })}
          className="btn btn-primary"
        >
          Create
        </button>
      </form>
      <Modal
        title="Resources"
        showModal={showTableModal}
        onClose={handleCloseTableModal}
      >
        <ResourcesTable
          filter={{ kind: dependencyKind }}
          onRawClick={handleTableRawClick}
        />
      </Modal>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={handleCloseResourceModal}
        showModal={showResourceModal}
        onSave={() => handleOnSaveResourceModal(selectedResource)}
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </>
  );
};

export default CreateResourceForm;
