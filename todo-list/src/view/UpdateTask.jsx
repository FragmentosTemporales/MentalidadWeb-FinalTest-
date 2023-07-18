import { useParams, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import "../App.css";
import { useContext, useEffect, useState } from "react";
import { Context } from "../store/Context";

function UpdateTask() {
  const { id } = useParams();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const { actions, store } = useContext(Context);
  const { tasks } = store;
  const [task, setTask] = useState({ task: "", description: "" });
  const navigate = useNavigate()
  
  const getTask = () => {
    let taskFind = tasks.find((task) => task.id === parseInt(id));
    setTask(taskFind);
  };
  useEffect(() => {
    getTask();
  });

  const onSubmit = (data) => {
    actions.updateTask(data, id);
    navigate("/");
  };

  return (
    <div className="body container-fluid d-flex justify-content-center">
      <div className="col-md-6 col-12 py-4">
        <div className="card shadow-sm">
          <form onSubmit={handleSubmit(onSubmit)} className="card-body">
            <div className="mb-3">
              <label htmlFor="task">Upgrade the Task</label>
              <input
                placeholder={task.task}
                maxLength={100}
                type="text"
                className="form-control rounded-0"
                {...register("task", { required: true })}
              />
              {errors.task && (
                <span className="text-danger">Task is required</span>
              )}
            </div>
            <div className="mb-3">
              <label htmlFor="description">Upgrade the Description</label>
              <input
                placeholder={task.description}
                maxLength={500}
                type="text"
                className="form-control rounded-0"
                {...register("description", { required: true })}
              />
              {errors.description && (
                <span className="text-danger">Description is required</span>
              )}
            </div>
            <div className="d-flex justify-content-center">
              <button
                style={{ background: "#7e799a" }}
                className="btn btn-submit rounded-5 text-white shadow"
              >
                SUBMIT
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default UpdateTask;
