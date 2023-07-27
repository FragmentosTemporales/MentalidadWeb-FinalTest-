import { Link } from "react-router-dom";
import { useContext } from "react";
import { Context } from "../store/Context";
import "../App.css";

function Navbar() {
  const { actions, store } = useContext(Context);
  const { token } = store;

  const handleClick = () => {
    actions.logout();
  };

  return (
    <nav className="navbar navbar-expand-lg">
      <div className="container-fluid px-4">
        <div className="dropdown">
          <button
            style={{ background: "#595959" }}
            className="btn text-white shadow-sm rounded-5 dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <i className="bi bi-list"></i>
          </button>
          <ul className="dropdown-menu">
            <li>
              {token ? <Link className="dropdown-item" to="/">
                <h6>Home</h6>
              </Link> : null}
            </li>
            <li>
            {token ? null : <Link className="dropdown-item" to="/register">
                <h6>Register</h6>
              </Link>}
            </li>
            <li>
              {token ? null : <Link className="dropdown-item" to="/login">
                <h6>Login</h6>
              </Link>}
            </li>
            <li>
              {token ? <Link className="dropdown-item" to="/user">
                <h6>Settings</h6>
              </Link> : null}
            </li>
          </ul>
        </div>
        <div className="logout">
          <button onClick={handleClick} className="btn btn-dark text-white rounded-5 shadow">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
