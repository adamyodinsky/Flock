import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import Alert from "../../general-components/Alert";
import Button from "../../general-components/Button";
import {
  BaseResourceSchema,
  Kind,
  ResourceFormData,
  kindValues,
  resourceFormSchema,
} from "../../resources_schemas";
import {
  ResourceSchemaService,
  ResourceService,
} from "../../services/resources_api";
import OptionsInput from "../OptionsInput";
import ToolsInput from "../ToolsInput";
import DependencyInput from "./DependencyInput";
// import { DevTool } from "@hookform/devtools";

interface OptionsRecord {
  [key: string]: any;
}

const CreateResourceForm = () => {
  const methods = useForm<ResourceFormData>({
    resolver: zodResolver(resourceFormSchema),
  });

  const {
    register,
    control,
    handleSubmit,
    setValue,
    formState: { errors, isValid },
  } = methods;

  const [error, setError] = useState([]);
  const [kind, setKind] = useState<string>();
  const [vendorList, setVendorList] = useState<string[]>([]);
  const [dependencyList, setDependencyList] = useState<string[]>([]);

  const schemaService = new ResourceSchemaService();
  const resourceService = new ResourceService();

  useEffect(() => {
    if (!kind) return;

    schemaService
      .get(kind)
      .then((response) => {
        setVendorList(response.data.vendor);
        setDependencyList(response.data.dependencies);
      })
      .catch((err) => setError(err.message));
  }, [kind]);

  const onSubmit = (data: ResourceFormData) => {
    console.log("Submitted");
    console.log(data);

    const transformedOptions = data.options?.reduce<OptionsRecord>(
      (acc, { key, value }) => {
        acc[key] = value;
        return acc;
      },
      {}
    );

    const resource: BaseResourceSchema = {
      apiVersion: "flock/v1",
      kind: data.kind,
      namespace: data.namespace,
      metadata: {
        name: data.name,
        description: data.description,
      },
      spec: {
        options: transformedOptions,
        vendor: data.vendor,
        tools: data.tools
          ? data.tools.map((tool) => ({
              name: tool.name,
              kind: tool.kind as Kind,
              namespace: tool.namespace,
            }))
          : undefined,
        dependencies: data.dependencies
          ? data.dependencies.map((dependency) => ({
              name: dependency.name,
              kind: dependency.kind as Kind,
              namespace: dependency.namespace,
            }))
          : undefined,
      },
    };

    console.log(resource);

    resourceService
      .post(resource)
      .then((_) => {
        setError([]);
      })
      .catch((err) => {
        setError(err.response.data.detail);
        console.log(err.response.data.detail);
      });
  };

  return (
    <>
      <Alert>
        {error.map((err, index) => (
          <pre key={index}>{err}</pre>
        ))}
      </Alert>
      <FormProvider {...methods}>
        <form className="form-control" onSubmit={handleSubmit(onSubmit)}>
          <div className="form-control m-1">
            <div className="m-1">
              <label className="form-label" htmlFor="name">
                <strong>Name</strong>
              </label>
              <input
                {...register("name")}
                id="name"
                type="text"
                className="form-control"
              />
              {errors.name && (
                <p className="text-danger">{errors.name.message}</p>
              )}
            </div>
            <div className="m-1">
              <label className="form-label" htmlFor="description">
                <strong>Description</strong>
              </label>
              <input
                {...register("description")}
                id="description"
                type="text"
                className="form-control"
              />
              {errors.description && (
                <p className="text-danger">{errors.description.message}</p>
              )}
            </div>
            <div className="m-1">
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
            <div className="m-1">
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
              {errors.kind && (
                <p className="text-danger">{errors.kind.message}</p>
              )}
            </div>
            <div className="m-1">
              <label className="form-label" htmlFor="vendor">
                <strong>Vendor</strong>
              </label>
              <select
                {...register("vendor")}
                id="vendor"
                className="form-select"
              >
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
          </div>
          <div className="m-1 form-control">
            <label className="form-label" htmlFor="dependencies">
              <h5>Options</h5>
            </label>
            <OptionsInput
              register={register}
              setValue={setValue}
              control={control}
            />
          </div>
          {dependencyList.length > 0 && (
            <div className="m-1 form-control">
              <label className="form-label" htmlFor="dependencies">
                <h5>Dependencies</h5>
              </label>
              <DependencyInput
                register={register}
                dependencyKindList={dependencyList}
                setValue={setValue}
              />
              {errors.dependencies && (
                <p className="text-danger">{errors.dependencies.message}</p>
              )}
            </div>
          )}
          {kind === "Agent" && (
            <div className="m-1 form-control">
              <label className="form-label" htmlFor="tools">
                <h5 className="">Tools</h5>
              </label>
              <ToolsInput
                register={register}
                setValue={setValue}
                control={control}
              />
              {errors.tools && (
                <p className="text-danger">{errors.tools?.message}</p>
              )}
            </div>
          )}
          <Button
            disabled={!isValid}
            color="success"
            additionalClasses="btn-lg"
            type="submit"
          >
            Create
          </Button>
        </form>
      </FormProvider>
      {/* <DevTool control={control} /> */}
    </>
  );
};

export default CreateResourceForm;
