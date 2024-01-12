import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import {
  DeploymentFormData,
  deploymentForm,
  deploymentKindValues,
} from "../../deployments_schemas";
import ConfigInput from "./ConfigInput";
import TargetResourceInput from "./TargetResourceInput";
import Button from "../../general-components/Button";

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

  const onSubmit = (data: DeploymentFormData) => {
    console.log("Submitted");
    console.log(data);
  };

  return (
    <>
      <FormProvider {...methods}>
        <form className="form-control m-2" onSubmit={handleSubmit(onSubmit)}>
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
              {deploymentKindValues.map((kind, index) => (
                <option key={index} value={kind}>
                  {kind}
                </option>
              ))}
            </select>
            {errors.deployment_kind && <span>This field is required</span>}
          </div>
          <div>
            <label htmlFor="target-resource">Target Resource</label>
            <TargetResourceInput />
          </div>
          <div>
            <label htmlFor="configuration">Configuration</label>
            <ConfigInput register={register} />
          </div>
          <div className="m-3">
            <Button
              color="success"
              additionalClasses="btn-lg"
              disabled={!isValid}
              type="submit"
            >
              Deploy
            </Button>
          </div>
        </form>
      </FormProvider>
    </>
  );
};

export default DeployerForm;
