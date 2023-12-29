const CreateResourceForm = () => {
  return (
    <form className="form-control">
      <div className="mb-3">
        <label className="form-label" htmlFor="name">
          Name
        </label>
        <input type="text" className="form-control"></input>
      </div>
    </form>
  );
};

export default CreateResourceForm;
