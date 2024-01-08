import "./App.css";
import CreateResourceForm from "./domain-components/CreateResourceForm/CreateResourceForm";
import ResourcesTablePage from "./domain-components/ResourcesTablePage";

function App() {
  return (
    <>
      <CreateResourceForm />
      <ResourcesTablePage />
    </>
  );
}

export default App;
