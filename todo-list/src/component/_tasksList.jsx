import "../App.css";
import { useContext, useEffect } from "react";
import { Context } from "../store/Context";
import { Link } from "react-router-dom";

function TasksList() {
  const { actions, store } = useContext(Context);
  const { tasks } = store;
  const onSubmit = (id) => {
    actions.deleteTask(id);
  };
  const handleClick = (id) => {
    actions.setCompleted(id);
    console.log(id);
  };

  useEffect(() => {}, [tasks]);

  const incompleteTasks = tasks.filter((task) => !task.is_completed);

  return (
    <div className="container-fluid d-flex justify-content-center">
      <div className="col-12 py-4">
        <h3 className="text-white">You have {incompleteTasks.length} pending tasks.</h3>
        <div className="card shadow-sm">
          {incompleteTasks.length > 0 ? (
            <div className="container-fluid">
              {incompleteTasks.map((task) => (
                <div className="row card-body shadow-sm" key={task.id}>
                  <div className="col-9">
                    <h3>{task.task}</h3>
                    <p>{task.description}</p>
                  </div>
                  <div className="d-flex justify-content-center col-3">
                    <div className="flex-column">
                      <Link
                        style={{ background: "#e2c08d" }}
                        to={"/update/" + task.id}
                        className="btn rounded-5 m-1 shadow w-20 text-white "
                      >
                        <i className="bi bi-arrow-clockwise"></i>
                      </Link>
                      <button
                        style={{ background: "#595959" }}
                        onClick={() => onSubmit(task.id)}
                        className="btn rounded-5 m-1 shadow w-20 text-white"
                      >
                        <i className="bi bi-trash3"></i>
                      </button>
                      <button
                        onClick={() => handleClick(task.id)}
                        className="btn btn-success rounded-5 m-1 shadow w-20 text-white"
                      >
                        <i className="bi bi-check-circle"></i>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="row">
              <div className="d-flex justify-content-center">
                <h3>No tasks to show...</h3>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TasksList;
