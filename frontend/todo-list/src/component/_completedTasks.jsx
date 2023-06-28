import "../App.css";
import { useContext, useEffect } from "react";
import { Context } from "../store/Context";

function CompletedTasksList() {
  const { actions, store } = useContext(Context);
  const { tasks } = store;
  const onSubmit = (id) => {
    actions.deleteTask(id);
  };
  const handleClick = (id) => {
    actions.setIncomplete(id);
  };
  useEffect(() => {}, [tasks]);

  const completedTasks = tasks.filter((task) => task.isCompleted);

  return (
    <div className="container-fluid d-flex justify-content-center">
      <div className="col-12 py-4">
        <h3 className="text-white">You have {completedTasks.length} completed tasks.</h3>
        <div className="card shadow-sm">
          {completedTasks.length > 0 ? (
            <div className="container-fluid">
              {completedTasks.map((task) => (
                <div className="row card-body shadow-sm" key={task.id}>
                  <div className="col-9">
                    <h3>{task.task}</h3>
                    <p>{task.description}</p>
                  </div>
                  <div className="d-flex justify-content-center col-3">
                    <div className="flex-column">
                      <button
                        style={{ background: "#595959" }}
                        onClick={() => onSubmit(task.id)}
                        className="btn rounded-5 m-1 shadow w-20 text-white"
                      >
                        <i className="bi bi-trash3"></i>
                      </button>
                      <button
                        onClick={() => handleClick(task.id)}
                        className="btn btn-danger rounded-5 m-1 shadow w-20 text-white"
                      >
                        <i className="bi bi-x-circle"></i>
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

export default CompletedTasksList;
