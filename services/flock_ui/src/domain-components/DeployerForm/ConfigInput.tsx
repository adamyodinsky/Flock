import yaml from "js-yaml";
import { ReactNode, useEffect, useState } from "react";
import { UseFormRegister } from "react-hook-form";
import {
  ConfigKind,
  ConfigResponseObj,
  DeploymentConfigData,
  DeploymentFormData,
  EnvData,
} from "../../deployments_schemas";
import Alert from "../../general-components/Alert";
import Button from "../../general-components/Button";
import Modal from "../../general-components/Modal";
import { ConfigService } from "../../services/deployments_api";
import ConfigsTable from "./ConfigsTable";

const apiConfigService = new ConfigService();
interface Props {
  register: UseFormRegister<DeploymentFormData>;
}
const ConfigInput = ({ register }: Props) => {
  const [idCounter, setIdCounter] = useState(0);
  const [showTableModal, setShowTableModal] = useState(false);
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [error, setError] = useState([]);
  const [isTableLoading, setIsTableLoading] = useState(false);
  const [configTableList, setConfigTableList] = useState<ConfigResponseObj[]>(
    []
  );
  useState<ConfigResponseObj>();
  const [selectedShallowResource, setSelectedShallowResource] =
    useState<ConfigResponseObj>();
  const [selectedResource, setSelectedResource] =
    useState<DeploymentConfigData>();
  const [savedResource, setSavedResource] = useState<DeploymentConfigData>();
  const [envList, SetEnvList] = useState<EnvData[]>([]);

  // const { fields, append, remove } = useFieldArray({
  //   control,
  //   name: "config.env",
  // });

  useEffect(() => {
    if (!savedResource) return;
    SetEnvList([...savedResource.env]);
  }, [savedResource]);

  useEffect(() => {
    if (!selectedShallowResource) return;
    apiConfigService
      .get(selectedShallowResource.id)
      .then((response) => {
        console.log(response.data);
        setSelectedResource(response.data);
        setError([]);
      })
      .catch((err) => {
        console.log(err);
        setError(err.response?.data.detail);
      });
  }, [selectedShallowResource]);

  const handleClickOnChoose = () => {
    setIsTableLoading(true);
    const { request, cancel } = apiConfigService.getAll(
      ConfigKind.DeploymentConfig
    );

    request
      .then((response) => {
        setConfigTableList(response.data.items);
        setError([]);
        setIsTableLoading(false);

        setTimeout(() => {
          setShowTableModal(true);
        }, 100);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.response.data.detail);
      });

    return () => cancel();
  };

  const handleClickOnAdd = (isSecret: boolean) => {
    console.log("clicked Add!");

    if (isSecret) {
      SetEnvList([
        ...envList,
        { name: "", valueFrom: { secretKeyRef: { name: "", key: "" } } },
      ]);
    } else {
      SetEnvList([...envList, { name: "", value: "" }]);
    }
  };

  const handleClickOnRemove = (indexToRemove: number) => {
    SetEnvList((currentEnvList) =>
      currentEnvList.filter((_, index) => index !== indexToRemove)
    );
  };

  const handleTableRawClick = (resource: ConfigResponseObj) => {
    setSelectedShallowResource(resource);
    setShowResourceModal(true);
  };

  const handleOnSaveResourceModal = () => {
    setSavedResource(selectedResource);
    setShowResourceModal(false);
    setShowTableModal(false);
  };

  const getModalFooterButtons = (): ReactNode => {
    return (
      <>
        <Button
          type="button"
          color="outline-primary"
          onClick={handleOnSaveResourceModal}
        >
          Save
        </Button>
      </>
    );
  };

  return (
    <>
      <Alert>
        {error.map((err) => (
          <pre>{err}</pre>
        ))}
      </Alert>
      <div className="form-control m-1">
        <div className="input-group m-1">
          <div className="m-2">
            <Button color="primary" onClick={handleClickOnChoose}>
              {isTableLoading && (
                <span
                  className="spinner-border spinner-border-sm me-2"
                  aria-hidden="true"
                />
              )}
              Find & Choose
            </Button>
            <span className="m-3">
              <Button
                color="outline-primary"
                onClick={() => handleClickOnAdd(false)}
              >
                Add Config
              </Button>
            </span>
            <span>
              <Button
                color="outline-primary"
                onClick={() => handleClickOnAdd(true)}
              >
                Add Secret
              </Button>
            </span>
          </div>
        </div>
        {envList.map((env, index) => (
          <div className="m-2 input-group">
            <input
              className="form-control"
              type="text"
              id="config_key"
              placeholder="Name"
              aria-label="key"
              defaultValue={env.name}
              // {...register(config.env[index].name)}
            />
            {"value" in env ? (
              <>
                <input
                  className="form-control"
                  type="text"
                  id="config_value"
                  aria-label="config_value"
                  placeholder="Value"
                  defaultValue={env.value}
                />
              </>
            ) : (
              <>
                <input
                  className="form-control"
                  type="text"
                  id="secret_name"
                  placeholder="Secret Name"
                  aria-label="secret_name"
                  defaultValue={env.valueFrom.secretKeyRef.name}
                />
                <input
                  className="form-control"
                  type="text"
                  id="secret_key"
                  placeholder="Secret Key"
                  aria-label="secret_key"
                  defaultValue={env.valueFrom.secretKeyRef.key}
                />
              </>
            )}
            <Button
              type="button"
              color="danger"
              onClick={() => handleClickOnRemove(index)}
            >
              Remove
            </Button>
          </div>
        ))}
      </div>
      <Modal
        title="Resources"
        showModal={showTableModal}
        onClose={() => setShowTableModal(false)}
        extraClassNames="modal-xl"
      >
        <ConfigsTable
          onRawClick={handleTableRawClick}
          configList={configTableList}
        />
      </Modal>
      <Modal
        title={selectedShallowResource?.name}
        onClose={() => setShowResourceModal(false)}
        showModal={showResourceModal}
        footerButtons={getModalFooterButtons()}
      >
        <pre>{yaml.dump(selectedShallowResource)}</pre>
      </Modal>
    </>
  );
};

export default ConfigInput;
