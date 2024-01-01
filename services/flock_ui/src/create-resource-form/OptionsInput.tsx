import {
  Control,
  UseFormRegister,
  UseFormSetValue,
  useFieldArray,
} from "react-hook-form";
import { ResourceFormData } from "../schemas";

type KeyValue = Record<string, string>[];

interface Props {
  register: UseFormRegister<ResourceFormData>;
  setValue: UseFormSetValue<ResourceFormData>;
  control: Control<ResourceFormData>;
}

const OptionsInput = ({ register, control }: Props) => {
  const { fields, append, remove } = useFieldArray({
    control,
    name: "options",
  });

  const handleClickAdd = () => {
    append({ key: "", value: "" });
  };

  return (
    <>
      <label>Options</label>
      <div className="m-1">
        <button
          className="btn btn-outline-primary"
          type="button"
          id="add-tool-button"
          onClick={() => handleClickAdd()}
        >
          Add Option
        </button>
      </div>
      {fields.map((field, index) => {
        const keys = Object.keys(field);
        const values = Object.values(field);
        return (
          <div key={index} className="form-control">
            <div className="input-group m-1">
              <input
                {...register(`options.${index}.key`)}
                type="text"
                className="form-control"
                placeholder="key"
                aria-label="key"
              />
              <input
                {...register(`options.${index}.value`)}
                type="text"
                className="form-control"
                placeholder="value"
                aria-label="value"
              />
              <button
                className="btn btn-outline-danger"
                type="button"
                id="add-tool-button"
                onClick={() => remove(index)}
              >
                Remove
              </button>
            </div>
          </div>
        );
      })}
    </>
  );
};

export default OptionsInput;
