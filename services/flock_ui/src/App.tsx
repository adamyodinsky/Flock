import "./App.css";
import CreateResourceForm from "./domain-components/CreateResourceForm/CreateResourceForm";
import DeployerForm from "./domain-components/DeployerForm/DeployerForm";
import ResourcesTablePage from "./domain-components/ResourcesTablePage";

function App() {
  return (
    <>
      <CreateResourceForm />
      <ResourcesTablePage />
      {/* <DeployerForm /> */}
    </>
  );
}

export default App;
