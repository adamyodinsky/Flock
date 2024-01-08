import { useEffect } from "react";
import {
  Control,
  UseFormRegister,
  UseFormSetValue,
  useFieldArray,
} from "react-hook-form";
import Button from "../general-components/Button";
import { ResourceFormData } from "../schemas";

interface Props {
  register: UseFormRegister<ResourceFormData>;
  setValue: UseFormSetValue<ResourceFormData>;
  control: Control<ResourceFormData>;
  initialOptions?: Record<string, any>;
}

const EditOptionsInput = ({
  register,
  control,
  initialOptions,
  setValue,
}: Props) => {
  const { fields, append, remove } = useFieldArray({
    control,
    name: "options",
  });

  useEffect(() => {
    const transformedOptions = Object.entries(initialOptions || {}).map(
      ([key, value]) => ({ key, value })
    );
    setValue("options", transformedOptions);
  }, []);

  const handleClickAdd = () => {
    append({ key: "", value: "" });
  };

  return (
    <>
      <div className="mb-3">
        <Button
          color="outline-primary"
          type="button"
          id="add-tool-button"
          onClick={() => handleClickAdd()}
        >
          Add Option
        </Button>
      </div>
      {fields.map((field, index) => {
        return (
          <div key={field.id} className="form-control">
            <div className="input-group m-1">
              <input
                {...register(`options.${index}.key`)}
                type="text"
                className="form-control"
                placeholder="key"
                aria-label="key"
                defaultValue={field.key}
              />
              <input
                {...register(`options.${index}.value`)}
                type="text"
                className="form-control"
                placeholder="value"
                aria-label="value"
                defaultValue={field.value}
              />
              <Button
                color="outline-danger"
                type="button"
                id="add-tool-button"
                onClick={() => remove(index)}
              >
                Remove
              </Button>
            </div>
          </div>
        );
      })}
    </>
  );
};

export default EditOptionsInput;
