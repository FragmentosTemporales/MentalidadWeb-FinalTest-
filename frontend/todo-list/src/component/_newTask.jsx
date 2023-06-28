import { useForm } from "react-hook-form";
import "../App.css";
import { useContext } from "react";
import { Context } from "../store/Context";

function NewTask() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const { actions } = useContext(Context);
    const onSubmit = (data) => {
        actions.newTask(data)
      };
      return (
        <div 
        style={{maxHeight: "250px"}}
        className="body container-fluid d-flex justify-content-center">
          <div className="col-12 py-4">
          <h3 className="text-white">Create a task</h3>
            <div className="card shadow-sm">
              <form onSubmit={handleSubmit(onSubmit)} className="card-body">
              <div className="mb-3">
                <label htmlFor="task">Write your Task</label>
                <input maxLength={100} type="text" className="form-control rounded-0" placeholder="Task" {...register("task", { required: true })}/>
                {errors.task && (
                    <span className="text-danger">Task is required</span>
                  )}
              </div>
              <div className="mb-3">
                <label htmlFor="description">Write your Description</label>
                <input maxLength={500} type="text" className="form-control rounded-0" placeholder="Description" {...register("description", { required: true })}/>
                {errors.description && (
                    <span className="text-danger">Description is required</span>
                  )}
              </div>
              <div className="d-flex justify-content-center">
              <button 
              style={{background:"#7e799a"}}
              className="btn btn-submit rounded-5 text-white shadow">SUBMIT</button>
              </div>
            </form>
            </div>
          </div>
        </div>
      );
}

export default NewTask;
