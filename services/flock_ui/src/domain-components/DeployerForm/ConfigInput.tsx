import { useState } from "react";
import { ConfigKind, ConfigResponseObj } from "../../deployments_schemas";
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
  const [selectedResource, setSelectedResource] = useState<ConfigResponseObj>();

  const handleClickOnChoose = () => {
    setIsTableLoading(true);
    const { request, cancel } = apiConfigService.getAll(
      ConfigKind.DeploymentConfig
    );

    request
      .then((response) => {
        console.log(response);
        // setConfigTableList(response.data);
        setError([]);
        setIsTableLoading(false);
        setShowTableModal(true);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.response?.data.detail);
      });

    return () => cancel();
  };

  const handleTableRawClick = (resource: ConfigResponseObj) => {
    setSelectedResource(resource);
    setShowResourceModal(true);
  };

  return (
    <>
      {/* <Alert>
        {error.map((err) => (
          <pre>{err}</pre>
        ))}
      </Alert> */}
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
          </div>
        </div>

        <div className="m-2 input-group">
          <input
            className="form-control"
            type="text"
            id="config_key"
            placeholder="key"
            aria-label="key"
          />
          <input
            className="form-control"
            type="text"
            id="config_value"
            placeholder="value"
            aria-label="value"
          />
        </div>
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
      {/* <Modal
        title={selectedResource?.metadata.name}
        onClose={() => setShowResourceModal(false)}
        showModal={showResourceModal}
        footerButtons={getModalFooterButtons()}
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal> */}
    </>
  );
};

export default ConfigInput;
