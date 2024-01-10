import { useState } from "react";
import Alert from "../../general-components/Alert";
import Button from "../../general-components/Button";

const ConfigInput = () => {
  const [showTableModal, setShowTableModal] = useState(false);
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [error, setError] = useState([]);
  const [isTableLoading, setIsTableLoading] = useState(false);
  const [configTableList, setConfigTableList] = useState([]);

  const handleClickOnChoose = () => {
    setIsTableLoading(true);
    const { request } = apiService.getAll({ kind: "" });

    request
      .then((response) => {
        setConfigTableList(response.data.items);
        setError([]);
        setIsTableLoading(false);
        setShowTableModal(true);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.response.data.detail);
      });
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
        <div className="m-2">
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
        <ResourcesTable
          onRawClick={handleClickTableRaw}
          resourceList={resourceTableList}
        />
      </Modal>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={() => setShowResourceModal(false)}
        showModal={showResourceModal}
        footerButtons={getModalFooterButtons()}
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </>
  );
};

export default ConfigInput;
