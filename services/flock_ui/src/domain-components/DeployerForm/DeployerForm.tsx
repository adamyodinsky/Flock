import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import {
  DeploymentFormData,
  deploymentForm,
  deploymentKindValues,
} from "../../deployments_schemas";
import TargetResourceInput from "./TargetResourceInput";

const DeployerForm = () => {
  const methods = useForm<DeploymentFormData>({
    resolver: zodResolver(deploymentForm),
  });

  const {
    register,
    control,
    handleSubmit,
    setValue,
    formState: { errors, isValid },
  } = methods;

  const [error, setError] = useState([]);

  return (
    <>
      <FormProvider {...methods}>
        <form className="form-control m-2">
          <div>
            <label className="form-label">Deployment Name</label>
            <input
              type="text"
              placeholder="Input a name..."
              className="form-control"
              {...register("deployment_name", { required: true })}
            />
            {errors.deployment_name && <span>This field is required</span>}
          </div>
          <div>
            <label className="form-label">Deployment Kind</label>
            <select
              className="form-select"
              {...register("deployment_kind", { required: true })}
            >
              {deploymentKindValues.map((kind) => (
                <option value={kind}>{kind}</option>
              ))}
            </select>
            {errors.deployment_kind && <span>This field is required</span>}
          </div>
          <div>
            <label htmlFor="target-resource">Target Resource</label>
            <TargetResourceInput />
          </div>
        </form>
      </FormProvider>
    </>
  );
};

export default DeployerForm;
