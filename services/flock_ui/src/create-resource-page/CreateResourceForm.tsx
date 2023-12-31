import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { ResourceFormData, kindValues, resourceFormSchema } from "../schemas";
import { ResourceSchemaService } from "../services/resourceService";
import DependencyInput from "./DependencyInput";
import ToolsInput from "./ToolsInput";

const CreateResourceForm = () => {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors, isValid },
  } = useForm<ResourceFormData>({ resolver: zodResolver(resourceFormSchema) });

  const [error, SetError] = useState("");
  const [kind, setKind] = useState<string>();
  const [vendorList, setVendorList] = useState<string[]>([]);
  const [dependencyList, setDependencyList] = useState<string[]>([]);

  useEffect(() => {
    if (!kind) return;

    const service = new ResourceSchemaService();
    service
      .get(kind)
      .then((response) => {
        setVendorList(response.data.vendor);
        setDependencyList(response.data.dependencies);
      })
      .catch((err) => SetError(err.message));
  }, [kind]);

  const onSubmit = (data: ResourceFormData) => {
    console.log(data);
    console.log("Submitted");
    console.log(errors);
  };

  return (
    <>
      <p className="text-danger">{error}</p>
      <form className="form-control" onSubmit={handleSubmit(onSubmit)}>
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
            <option value="" disabled selected>
              Select Kind
            </option>

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
            <option value="" disabled selected>
              Select Vendor
            </option>

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
            register={register}
            dependencyKindList={dependencyList}
            setValue={setValue}
          />
          {/* <Controller
            name="dependencies"
            control={control}
            render={({ field }) => (
              <DependencyInput {...field} dependencyKindList={dependencyList} />
            )}
          /> */}
          {errors.dependencies && (
            <p className="text-danger">{errors.dependencies.message}</p>
          )}
        </div>
        {kind === "Agent" && (
          <div className="mb-3">
            <label className="form-label" htmlFor="tools">
              <strong>Tools</strong>
            </label>
            <ToolsInput />
            {errors.tools && (
              <p className="text-danger">{errors.tools?.message}</p>
            )}
          </div>
        )}
        <button disabled={!isValid} className="btn btn-primary" type="submit">
          Create
        </button>
      </form>
    </>
  );
};

export default CreateResourceForm;
