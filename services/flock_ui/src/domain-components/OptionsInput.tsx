import { useEffect, useState } from "react";
import { useFormContext } from "react-hook-form";
import Button from "../general-components/Button";
import { ResourceFormData } from "../schemas";

interface OptionEntry {
  key: string;
  value: string;
}

interface OptionsRecord {
  [key: string]: string;
}

const OptionsInput = ({ register }: { register: any }) => {
  const { setValue, getValues } = useFormContext<ResourceFormData>();
  const initialOptions = Object.entries(getValues("options") || {}).map(
    ([key, value]) => ({ key, value })
  );
  const [optionsEntries, setOptionsEntries] =
    useState<OptionEntry[]>(initialOptions);

  useEffect(() => {
    const optionsRecord = optionsEntries.reduce<OptionsRecord>(
      (acc, { key, value }) => {
        if (key) acc[key] = value;
        return acc;
      },
      {} as OptionsRecord
    ); // Explicitly type the initial value
    setValue("options", optionsRecord);
  }, [optionsEntries, setValue]);

  const handleAddOption = () => {
    setOptionsEntries([...optionsEntries, { key: "", value: "" }]);
  };

  const handleRemoveOption = (index: number) => {
    const updatedOptions = optionsEntries.filter((_, i) => i !== index);
    setOptionsEntries(updatedOptions);
  };

  const handleOptionChange = (index: number, key: string, value: string) => {
    const updatedOptions = [...optionsEntries];
    updatedOptions[index] = { key, value };
    setOptionsEntries(updatedOptions);
  };

  return (
    <>
      <div className="mb-3">
        <Button color="outline-primary" type="button" onClick={handleAddOption}>
          Add Option
        </Button>
      </div>
      {optionsEntries.map(({ key, value }, index) => (
        <div key={index} className="form-control">
          <div className="input-group m-1">
            <input
              type="text"
              className="form-control"
              placeholder="Key"
              value={key}
              onChange={(e) => handleOptionChange(index, e.target.value, value)}
            />
            <input
              {...register(`options.${key}`)}
              type="text"
              className="form-control"
              placeholder="Value"
              value={value}
              onChange={(e) => handleOptionChange(index, key, e.target.value)}
            />
            <Button
              color="outline-danger"
              type="button"
              onClick={() => handleRemoveOption(index)}
            >
              Remove
            </Button>
          </div>
        </div>
      ))}
    </>
  );
};

export default OptionsInput;
