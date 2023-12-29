import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  Kind,
  ResourceFormData,
  kindValues,
  resourceFormSchema,
} from "../schemas";
import { ResourceSchemaService } from "../services/resourceService";

interface Props {
  onSubmit: (data: ResourceFormData) => void;
}

const CreateResourceForm = (props: Props) => {
  const [kind, setKind] = useState<string>(Kind.Embedding);
  const [vendorList, setVendorList] = useState<string[]>([]);
  const [dependencyList, setDependencyList] = useState<string[]>([]);

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
        <select {...register("vendor")} id="vendor" className="form-control">
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
        {dependencyList.map((val) => (
          <select
            id={val}
            className="form-control"
            value=""
            {...register("dependencies")}
          >
            <option key={val} value={val}>
              {val}
            </option>
          </select>
        ))}
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
