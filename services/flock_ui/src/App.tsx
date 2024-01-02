import "./App.css";
import CreateResourceForm from "./create-resource-form/CreateResourceForm";
import ResourcesTable from "./create-resource-form/ResourcesTable";

function App() {
  return (
    <>
      <CreateResourceForm />
      <ResourcesTable filter={{}} onRawClick={() => {}} />
    </>
  );
}

export default App;
