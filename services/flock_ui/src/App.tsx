import "./App.css";
import CreateResourceForm from "./create-resource-form/CreateResourceForm";
import ResourcesTable from "./create-resource-form/ResourcesTable";
import { BaseResourceSchema } from "./schemas";

function App() {
  const handleResourceEdit = (resource: BaseResourceSchema) => {
    console.log("Delete");
    console.log(resource);
    // This should open up a modal with the resource form and the resource data filled in and ready for editing

    // send put request to resource service
  };

  const handleResourceDelete = (resource: BaseResourceSchema) => {
    console.log("Delete");
    console.log(resource);
    // get resource id
    // send delete request to resource service
  };

  return (
    <>
      <CreateResourceForm />
      <ResourcesTable filter={{}} />
    </>
  );
}

export default App;
