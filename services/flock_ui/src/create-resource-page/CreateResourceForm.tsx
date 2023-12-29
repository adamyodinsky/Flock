import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  Kind,
  ResourceFormData,
  kindValues,
  resourceFormSchema,
} from "../schemas";
import ResourceSchemaService from "../services/resourceService";

interface Props {
  onSubmit: (data: ResourceFormData) => void;
}

const CreateResourceForm = (props: Props) => {
  const [kind, setKind] = useState<string>(Kind.Embedding);
  const [namespace, setNamespace] = useState("default");
  const [vendorList, setVendorList] = useState<string[]>([]);
  const [vendor, setVendor] = useState<string>("");
  const [dependencyList, setDependencyList] = useState<string[]>([]);
  const [dependency, setDependency] = useState<string>("");

  useEffect(() => {
    ResourceSchemaService.get(kind).then((response) => {
      setVendorList(response.data.data.vendor);
      setDependencyList(response.data.data.dependencies);
    });
  }, [kind]);

  useEffect(() => {
    setVendor(vendorList[0]);
  }, [vendorList, dependencyList]);

  // TODO: debug, can remove later before production
  useEffect(() => {
    console.log(kind);
    console.log(vendor);
  }, [vendor]);

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<ResourceFormData>({ resolver: zodResolver(resourceFormSchema) });

  const onSubmit = (data: ResourceFormData) => {
    props.onSubmit(data);
  };

  return (
    <form className="form-control">
      <div className="mb-3">
        <label className="form-label" htmlFor="name">
          Name
        </label>
        <input
          {...register("name")}
          id="name"
          type="text"
          className="form-control"
          onChange={(event) => setNamespace(event.target.value)}
        ></input>
        {errors.name && <p className="text-danger">{errors.name.message}</p>}
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="description">
          Description
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
          Namespace
        </label>
        <select
          {...register("namespace")}
          id="namespace"
          className="form-control"
        >
          {/* this should be fetched dynamically */}
          <option value="default">default</option>
        </select>
        {errors.namespace && (
          <p className="text-danger">{errors.namespace.message}</p>
        )}
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="kind">
          Kind
        </label>
        <select
          {...register("kind")}
          id="kind"
          className="form-control"
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
          Vendor
        </label>
        <select
          {...register("vendor")}
          id="vendor"
          className="form-control"
          onChange={(event) => setVendor(event.target.value)}
        >
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
          Dependencies
        </label>
        <select
          {...register("dependencies")}
          id="dependencies"
          className="form-control"
          onChange={(event) => setDependency(event.target.value)}
        >
          {dependencyList.map((val) => (
            <option key={val} value={val}>
              {val}
            </option>
          ))}
        </select>
        {errors.dependencies && (
          <p className="text-danger">{errors.dependencies.message}</p>
        )}
      </div>
      <button
        // disabled={!isValid}
        onClick={handleSubmit((data) => {
          console.log(data);
        })}
        className="btn btn-primary"
      >
        Create
      </button>
    </form>
  );
};

export default CreateResourceForm;
