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
      {fields.map((e, index) => {
        return (
          <div key={index} className="form-control">
            <div className="input-group m-1">
              <input
                {...register(`options.${index}.key`)}
                type="text"
                className="form-control"
                placeholder="key"
                aria-label="key"
                defaultValue={e.key}
              />
              <input
                {...register(`options.${index}.value`)}
                type="text"
                className="form-control"
                placeholder="value"
                aria-label="value"
                defaultValue={e.value}
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

export default OptionsInput;
