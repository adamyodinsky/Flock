import yaml from "js-yaml";
import { ReactNode, useState } from "react";
import Button from "../../general-components/Button";
import Modal from "../../general-components/Modal";
import { BaseResourceSchema } from "../../resources_schemas";
import { ResourceService } from "../../services/resources_api";
import ResourcesTable from "../ResourcesTable";
const apiService = new ResourceService();

const TargetResourceInput = () => {
  const [targetKind, setTargetKind] = useState("Agent");
  const [showTableModal, setShowTableModal] = useState(false);
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();
  const [resourceTableList, setResourceTableList] = useState<
    BaseResourceSchema[]
  >([]);
  const [error, setError] = useState([]);
  const [isTableLoading, setIsTableLoading] = useState(false);
  const [targetResource, setTargetResource] = useState<BaseResourceSchema>();

  const handleClickOnChoose = () => {
    setIsTableLoading(true);
    const { request } = apiService.getAll({ kind: targetKind });

    request
      .then((response) => {
        setResourceTableList(response.data.items);
        setError([]);
        setShowTableModal(true);
        setIsTableLoading(false);
      })
      .catch((err) => {
        if (err.message !== "canceled") setError(err.response.data.detail);
      });
  };

  const handleClickTableRaw = (resource: BaseResourceSchema) => {
    setSelectedResource(resource);
    setShowResourceModal(true);
  };

  const handleOnSaveResourceModal = (e: BaseResourceSchema | undefined) => {
    if (!e) return;

    setTargetResource(e);
    setShowResourceModal(false);
    setShowTableModal(false);
  };

  const getModalFooterButtons = (): ReactNode => {
    return (
      <>
        <Button
          type="button"
          color="outline-primary"
          onClick={() => handleOnSaveResourceModal(selectedResource)}
        >
          Save
        </Button>
      </>
    );
  };

  return (
    <>
      <div className="form-control m-1">
        <div className="input-group m-1">
          <div className="m-2">
            <Button onClick={handleClickOnChoose}>Find & Choose</Button>
          </div>
          <select
            id="target-resource"
            className="form-select"
            onChange={(event) => setTargetKind(event.target.value)}
          >
            <option value="Agent">Agent</option>
            <option value="WebScraper">WebScraper</option>
          </select>
        </div>
        <div className="m-2">
          <input
            className="form-control"
            type="text"
            id="target_name"
            placeholder="Name"
            aria-label="target name"
            defaultValue={targetResource?.metadata.name}
            readOnly
          />
          <input
            className="form-control"
            type="text"
            id="target_name"
            placeholder="Namespace"
            aria-label="target namespace"
            defaultValue={targetResource?.namespace}
            readOnly
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

export default TargetResourceInput;
