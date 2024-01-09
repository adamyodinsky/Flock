import yaml from "js-yaml";
import { ReactNode } from "react";
import Modal from "../general-components/Modal";
import ResourcesTable from "./ResourcesTable";

interface Props {
  showTableModal: boolean;
  showResourceModal: boolean;
  resourceTableList: any[];
  selectedResource: any;
  handleCloseTableModal: () => void;
  handleTableRawClick: (resource: any) => void;
  handleCloseResourceModal: () => void;
  getModalFooterButtons: () => ReactNode;
}

const TablesModal = ({
  showTableModal,
  showResourceModal,
  resourceTableList,
  selectedResource,
  handleCloseTableModal,
  handleTableRawClick,
  handleCloseResourceModal,
  getModalFooterButtons,
}: Props) => {
  return (
    <div>
      <Modal
        title="Resources"
        showModal={showTableModal}
        onClose={handleCloseTableModal}
        extraClassNames="modal-xl"
      >
        <ResourcesTable
          onRawClick={handleTableRawClick}
          resourceList={resourceTableList}
        />
      </Modal>
      <Modal
        title={selectedResource?.metadata.name}
        onClose={handleCloseResourceModal}
        showModal={showResourceModal}
        footerButtons={getModalFooterButtons()}
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal>
    </div>
  );
};

export default TablesModal;
