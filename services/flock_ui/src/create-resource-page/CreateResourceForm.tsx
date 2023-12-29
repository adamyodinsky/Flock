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

const CreateResourceForm = () => {
  const [vendors, setVendors] = useState<string[]>([]);
  const [kind, setKind] = useState<Kind>(Kind.Embedding);

  useEffect(() => {
    console.log(kind);
    console.log(vendors);
    ResourceSchemaService.get(kind).then((response) => {
      setVendors(response.data.vendor);
    });
  }, [kind]);

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<ResourceFormData>({ resolver: zodResolver(resourceFormSchema) });

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
          {kindValues.map((kind) => (
            <option key={kind} value={kind}>
              {kind}
            </option>
          ))}
        </select>
        {errors.kind && <p className="text-danger">{errors.kind.message}</p>}
      </div>
      <button
        disabled={!isValid}
        onClick={handleSubmit((data) => {
          console.log(data);
        })}
        className="btn btn-primary"
      >
        Submit
      </button>
    </form>
  );
};

export default CreateResourceForm;
