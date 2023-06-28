import { useForm } from "react-hook-form";
import '../App.css'
import { useContext } from "react";
import { Context } from '../store/Context'
import { useNavigate } from "react-router-dom";

function Register() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { actions } = useContext(Context);
  const navigate = useNavigate()

  const onSubmit = (data) => {
    actions.userRegister(data, navigate);
  };

  return (
    <div className="body container-fluid d-flex justify-content-center">
      <div className="col-md-4 col-12 py-4">
        <div className="card shadow-sm">
          <form onSubmit={handleSubmit(onSubmit)} className="card-body">
          <div className="mb-3">
            <label htmlFor="username">Write your Username</label>
            <input maxLength={50} type="text" className="form-control rounded-0" placeholder="Username" {...register("username", { required: true })}/>
            {errors.username && (
                <span className="text-danger">Username is required</span>
              )}
          </div>
          <div className="mb-3">
            <label htmlFor="email">Write your Email</label>
            <input maxLength={50} type="email" className="form-control rounded-0" placeholder="Email" {...register("email", {
                  required: true,
                  pattern: /^\S+@\S+$/i,
                })}/>
                {errors.email && (
                <span className="text-danger">Valid email is required</span>
              )}
          </div>
          <div className="mb-3">
            <label htmlFor="password">Write your Password</label>
            <input maxLength={20} type="password" className="form-control rounded-0" placeholder="Password" {...register("password", { required: true })}/>
            {errors.password && (
                <span className="text-danger">Password is required</span>
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

export default Register;
