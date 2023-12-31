import yaml from "js-yaml";
import { useState } from "react";
import Modal from "../components/Modal";
import { BaseResourceSchema } from "../schemas";
import CreateResourceForm from "./CreateResourceForm";
import ResourcesTable from "./ResourcesTable";

const CreateResourcePage = () => {
  const [selectedResource, setSelectedResource] =
    useState<BaseResourceSchema>();
  const [showResourceModal, setShowResourceModal] = useState(false);

  const handleCloseResourceModal = () => {
    setShowResourceModal(false);
  };

  const handlingOnClick = (e: BaseResourceSchema) => {
    setSelectedResource(e);
  };

  return (
    <>
      <CreateResourceForm />
      {/* <ResourcesTable filter={{}} onRawClick={handlingOnClick} /> */}
      {/* <Modal
        title={selectedResource?.metadata.name}
        onClose={handleCloseResourceModal}
        showModal={showResourceModal}
        saveButtonText="Save Choice"
      >
        <pre>{yaml.dump(selectedResource)}</pre>
      </Modal> */}
    </>
  );
};

export default CreateResourcePage;
