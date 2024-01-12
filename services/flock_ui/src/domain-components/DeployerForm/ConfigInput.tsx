import yaml from "js-yaml";
import { ReactNode, useEffect, useState } from "react";
import {
  ConfigKind,
  ConfigResponseObj,
  DeploymentConfigData,
} from "../../deployments_schemas";
import Alert from "../../general-components/Alert";
import Button from "../../general-components/Button";
import Modal from "../../general-components/Modal";
import { ConfigService } from "../../services/deployments_api";
import ConfigsTable from "./ConfigsTable";

const apiConfigService = new ConfigService();

const ConfigInput = () => {
  const [showTableModal, setShowTableModal] = useState(false);
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [error, setError] = useState([]);
  const [isTableLoading, setIsTableLoading] = useState(false);
  const [configTableList, setConfigTableList] = useState<ConfigResponseObj[]>(
    []
  );
  const [selectedShallowResource, setSelectedShallowResource] =
    useState<ConfigResponseObj>();
  const [selectedResource, setSelectedResource] =
    useState<DeploymentConfigData>();

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

  const handleClickOnAdd = () => {
    console.log("clicked Add!");
  };

  const handleTableRawClick = (resource: ConfigResponseObj) => {
    setSelectedShallowResource(resource);
    setShowResourceModal(true);
  };

  const handleOnSaveResourceModal = (e: ConfigResponseObj | undefined) => {
    if (!e) return;

    setSelectedShallowResource(e);
    setShowResourceModal(false);
    setShowTableModal(false);
  };

  const getModalFooterButtons = (): ReactNode => {
    return (
      <>
        <Button
          type="button"
          color="outline-primary"
          onClick={() => handleOnSaveResourceModal(selectedShallowResource)}
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
            <Button onClick={handleClickOnChoose}>
              {isTableLoading && (
                <span
                  className="spinner-border spinner-border-sm me-2"
                  aria-hidden="true"
                />
              )}
              Find & Choose
            </Button>
            <Button onClick={handleClickOnAdd}>Add</Button>
          </div>
        </div>
        {selectedResource?.env.map((env) => (
          <div className="m-2 input-group">
            <input
              className="form-control"
              type="text"
              id="config_key"
              placeholder="Name"
              aria-label="key"
              defaultValue={env.name}
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
