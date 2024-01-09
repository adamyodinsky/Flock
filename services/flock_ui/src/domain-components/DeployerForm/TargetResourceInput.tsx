import yaml from "js-yaml";
import { useState } from "react";
import Button from "../../general-components/Button";
import Modal from "../../general-components/Modal";
import { BaseResourceSchema } from "../../resources_schemas";
import ResourcesTable from "../ResourcesTable";
import { set } from "react-hook-form";

const TargetResourceInput = () => {
  const [targetKind, setTargetKind] = useState("Agent");
  const [showTableModal, setShowTableModal] = useState(false);
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();

  const handleClickOnChoose = () => {
    console.log("Clicked on Choose");
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
            readOnly
          />
          <input
            className="form-control"
            type="text"
            id="target_name"
            placeholder="Namespace"
            aria-label="target namespace"
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
          onRawClick={() => console.log("clicked raw!")}
          resourceList={[]}
        />
      </Modal>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={() => setShowResourceModal(false)}
        showModal={showResourceModal}
        // footerButtons={getModalFooterButtons()}
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </>
  );
};

export default TargetResourceInput;
