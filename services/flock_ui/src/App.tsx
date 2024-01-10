import "./App.css";
import CreateResourceForm from "./domain-components/CreateResourceForm/CreateResourceForm";
import DeployerForm from "./domain-components/DeployerForm/DeployerForm";
import ResourcesTablePage from "./domain-components/ResourcesTablePage";
import Footer from "./general-components/Fotter";
import Header from "./general-components/Header";

function App() {
  return (
    <>
      <>
        <h1 className="m-3">Flock</h1>
        <p className="m-3">Empower Your Intelligence, Scale Your Vision</p>
        <br />
        {/* <Header /> */}
        <main role="main" className="container mt-4">
          <div className="starter-template">
            <div className="m-3">
              <h2 className="m-2">Create Resource</h2>
              <CreateResourceForm />
            </div>
            <br />
            <div className="m-3">
              <h2 className="m-2">Resources Table</h2>
              <ResourcesTablePage />
            </div>
            <br />
            <div className="m-3">
              <h2 className="m-2">Deploy</h2>
              <DeployerForm />
            </div>
          </div>
        </main>
        <Footer />
      </>
    </>
  );
}

export default App;
