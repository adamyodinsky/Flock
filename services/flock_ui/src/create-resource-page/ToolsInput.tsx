import yaml from "js-yaml";
import { useState } from "react";
import Modal from "../components/Modal";
import { BaseResourceSchema } from "../schemas";
import { ResourceParams } from "../services/resourceService";
import ResourcesTable from "./ResourcesTable";

interface Tool {
  name?: string;
  namespace?: string;
  kind?: string;
  id?: string;
}

const ToolsInput = () => {
  const [showTableModal, setShowTableModal] = useState(false);
  const [tableFilter, setTableFilter] = useState<ResourceParams>({});
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [toolsList, setToolsList] = useState<Tool[]>([]);
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();

  const handleCloseTableModal = () => {
    setShowTableModal(false);
  };

  const handleTableRawClick = (resource: BaseResourceSchema) => {
    setSelectedResource(resource);
    setShowResourceModal(true);
  };

  const handleCloseResourceModal = () => {
    setShowResourceModal(false);
  };

  const handleClickAdd = (filter: ResourceParams) => {
    setTableFilter(filter);
    setShowTableModal(true);
  };

  const handleClickRemove = (tool: Tool) => {
    setToolsList(toolsList.filter((e) => e.id !== tool.id));
  };

  const handleOnSaveResourceModal = (e: BaseResourceSchema | undefined) => {
    if (!e) return;

    setToolsList([
      ...toolsList,
      { name: e.metadata.name, kind: e.kind, namespace: e.namespace, id: e.id },
    ]);
    setShowResourceModal(false);
    setShowTableModal(false);
  };

  return (
    <>
      <div className="mb-3">
        <button
          className="btn btn-outline-primary"
          type="button"
          id="add-tool-button"
          onClick={() => handleClickAdd({ category: "tool" })}
        >
          Add Tool
        </button>
      </div>
      {toolsList.map((tool, index) => {
        const name = tool.name || "";
        const namespace = tool.namespace || "";
        const kind = tool.kind || "";

        return (
          <div key={index} className="form-control">
            <div className="input-group mb-3">
              <input
                type="text"
                className="form-control"
                placeholder="Kind"
                aria-label="Kind"
                value={kind}
                readOnly
              />
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                aria-label="Name"
                value={name}
                readOnly
              />
              <input
                type="text"
                className="form-control"
                placeholder="Namespace"
                aria-label="Namespace"
                value={namespace}
                readOnly
              />
              <button
                className="btn btn-outline-danger"
                type="button"
                id="add-tool-button"
                onClick={() => handleClickRemove(tool)}
              >
                Remove
              </button>
            </div>
          </div>
        );
      })}
      <Modal
        title="Resources"
        showModal={showTableModal}
        onClose={handleCloseTableModal}
        extraClassNames="modal-xl"
      >
        <ResourcesTable filter={tableFilter} onRawClick={handleTableRawClick} />
      </Modal>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={handleCloseResourceModal}
        showModal={showResourceModal}
        onSave={() => handleOnSaveResourceModal(selectedResource)}
        saveButtonText="Save Choice"
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </>
  );
};

export default ToolsInput;
