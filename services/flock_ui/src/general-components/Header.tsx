const Header = () => {
  return (
    <header className="m-2">
      <nav className="navbar navbar-expand-lg m-2">
        <a className="navbar-brand" href="#">
          Flock
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item active">
              <a className="nav-link" href="#">
                Home <span className="sr-only">(current)</span>
              </a>
            </li>
            {/* Add additional navigation links here */}
          </ul>
        </div>
      </nav>
    </header>
  );
};

export default Header;
