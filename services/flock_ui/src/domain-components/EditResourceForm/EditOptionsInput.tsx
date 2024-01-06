import { useEffect } from "react";
import {
  Control,
  UseFormRegister,
  UseFormSetValue,
  useFieldArray,
} from "react-hook-form";
import Button from "../../general-components/Button";
import { ResourceFormData } from "../../schemas";

interface Props {
  register: UseFormRegister<ResourceFormData>;
  setValue: UseFormSetValue<ResourceFormData>;
  control: Control<ResourceFormData>;
  options?: Record<string, any>;
}

const EditOptionsInput = ({ register, control, options }: Props) => {
  const { append, remove } = useFieldArray({
    control,
    name: "options",
  });

  useEffect(() => {
    console.log("options");
    console.log(options);
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
      {options &&
        Object.entries(options).map(([key, value], index) => {
          console.log("key");
          console.log(key);
          console.log("value");
          console.log(value);

          return (
            <div key={index} className="form-control">
              <div className="input-group m-1">
                <input
                  {...register(`options.${index}.key`)}
                  type="text"
                  className="form-control"
                  placeholder="key"
                  aria-label="key"
                  defaultValue={key}
                />
                <input
                  {...register(`options.${index}.value`)}
                  type="text"
                  className="form-control"
                  placeholder="value"
                  aria-label="value"
                  defaultValue={value}
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
