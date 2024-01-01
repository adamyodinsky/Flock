import "./App.css";
import CreateResourceForm from "./create-resource-form/CreateResourceForm";
import ResourcesTable from "./create-resource-form/ResourcesTable";
import { BaseResourceSchema } from "./schemas";

function App() {
  return (
    <>
      <CreateResourceForm />
      <ResourcesTable
        filter={{}}
        onRawClick={function (e: BaseResourceSchema): void {
          throw new Error("Function not implemented.");
        }}
      />
    </>
  );
}

export default App;
