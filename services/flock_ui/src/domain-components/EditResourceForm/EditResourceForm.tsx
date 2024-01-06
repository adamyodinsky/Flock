import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import Alert from "../../general-components/Alert";
import Button from "../../general-components/Button";
// import { DevTool } from "@hookform/devtools";

import {
  BaseResourceSchema,
  Kind,
  OptionsRecord,
  ResourceFormData,
  resourceFormSchema,
} from "../../schemas";
import {
  ResourceSchemaService,
  ResourceService,
} from "../../services/services";
import EditDependencyInput from "./EditDependencyInput";
import EditOptionsInput from "./EditOptionsInput";
import EditToolsInput from "./EditToolsInput";

interface Props {
  resourceToEdit: BaseResourceSchema;
}

const EditResourceForm = ({ resourceToEdit }: Props) => {
  const {
    watch,
    register,
    control,
    handleSubmit,
    setValue,
    formState: { errors, isValid },
  } = useForm<ResourceFormData>({ resolver: zodResolver(resourceFormSchema) });

  const [error, setError] = useState([]);
  const [vendorList, setVendorList] = useState<string[]>([]);
  const [dependencyKindsList, setDependencyKindsList] = useState<string[]>([]);
  const schemaService = new ResourceSchemaService();
  const resourceService = new ResourceService();

  useEffect(() => {
    console.log("Form Validation Errors", errors);
    const allFieldValues = watch();
    console.log("All Form Values", allFieldValues);
  }, [errors, watch]);

  useEffect(() => {
    schemaService
      .get(resourceToEdit.kind)
      .then((response) => {
        setVendorList(response.data.vendor);
        setDependencyKindsList(response.data.dependencies);
      })
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    setValue("name", resourceToEdit.metadata.name);
    setValue("namespace", resourceToEdit.namespace);
    setValue("kind", resourceToEdit.kind);
    setValue("description", resourceToEdit.metadata.description);
    setValue("vendor", resourceToEdit.spec.vendor);
    setValue("tools", resourceToEdit.spec.tools);
  }, []);

  const onSubmit = (data: ResourceFormData) => {
    console.log(data);
    console.log("Form Errors", errors);

    const transformedOptions = data.options?.reduce<OptionsRecord>(
      (acc, { key, value }) => {
        acc[key] = value;
        return acc;
      },
      {}
    );

    const resource: BaseResourceSchema = {
      apiVersion: "flock/v1",
      kind: resourceToEdit.kind,
      namespace: resourceToEdit.namespace,
      id: resourceToEdit.id,
      metadata: {
        name: resourceToEdit.metadata.name,
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
          : [],
        dependencies: data.dependencies
          ? data.dependencies.map((dependency) => ({
              name: dependency.name,
              kind: dependency.kind as Kind,
              namespace: dependency.namespace,
            }))
          : [],
      },
    };

    console.log(resource);

    resourceService
      .put(resource)
      .then((res) => {
        console.log(res);
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
        {error.map((err) => (
          <pre>{err}</pre>
        ))}
      </Alert>
      <form className="form-control" onSubmit={handleSubmit(onSubmit)}>
        <div className="form-control m-1">
          <div className="m-1">
            <div>
              <input
                {...register("name")}
                id="name"
                type="text"
                className="form-control"
                hidden
                readOnly
                defaultValue={resourceToEdit.metadata.name}
              />
              <input
                {...register("namespace")}
                id="namespace"
                type="text"
                className="form-control"
                hidden
                readOnly
                defaultValue={resourceToEdit.namespace}
              />
            </div>
            <input
              {...register("kind")}
              id="kind"
              type="text"
              className="form-control"
              hidden
              readOnly
              defaultValue={resourceToEdit.kind}
            />
            <label htmlFor="description">
              <strong>Description</strong>
            </label>
            <input
              {...register("description")}
              id="description"
              type="text"
              className="form-control"
              defaultValue={resourceToEdit.metadata.description}
            ></input>
            {errors.description && (
              <p className="text-danger">{errors.description.message}</p>
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
              defaultValue={resourceToEdit.spec.vendor}
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
        </div>
        <div className="m-1 form-control">
          <label className="form-label" htmlFor="dependencies">
            <h5>Options</h5>
          </label>
          <EditOptionsInput
            register={register}
            setValue={setValue}
            control={control}
            initialOptions={resourceToEdit.spec.options}
          />
        </div>
        {dependencyKindsList.length > 0 && (
          <div className="m-1 form-control">
            <label className="form-label" htmlFor="dependencies">
              <h5>Dependencies</h5>
            </label>
            <EditDependencyInput
              register={register}
              dependencyKindList={dependencyKindsList}
              setValue={setValue}
              initValue={resourceToEdit.spec.dependencies}
            />
            {errors.dependencies && (
              <p className="text-danger">{errors.dependencies.message}</p>
            )}
          </div>
        )}
        {resourceToEdit.kind === "Agent" && (
          <div className="m-1 form-control">
            <label className="form-label" htmlFor="tools">
              <h5 className="">Tools</h5>
            </label>
            <EditToolsInput
              register={register}
              setValue={setValue}
              control={control}
              initValue={resourceToEdit.spec.tools}
            />
            {errors.tools && (
              <p className="text-danger">{errors.tools?.message}</p>
            )}
          </div>
        )}
        <Button
          disabled={!isValid}
          color="outline-primary"
          additionalClasses="btn-lg"
          type="submit"
        >
          Update
        </Button>
      </form>
      {/* <DevTool control={control} /> */}
    </>
  );
};

export default EditResourceForm;
