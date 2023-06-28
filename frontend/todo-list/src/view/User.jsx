import { useForm } from "react-hook-form";
import { useContext } from "react";
import { Context } from "../store/Context";
import { useNavigate } from "react-router-dom";
function User() {
  const { store, actions } = useContext(Context);
  const { username } = store;
  const navigate = useNavigate()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onSubmit = (data) => {
    actions.setUsername(data, navigate);
  };
  const handleClick = () => {
    actions.disabledUser()
  };
  return (
    <div className="body container-fluid d-flex justify-content-center">
      <div className="col-md-4 col-12 py-4">
        <div className="card shadow-sm">
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="shadow card-body p-4"
          >
            <div className="mb-3">
              <h6 className="text-center">Want to change your username?</h6>
              <input
                maxLength={50}
                type="text"
                className="form-control rounded-0"
                placeholder={username}
                {...register("username", { required: true })}
              />
              {errors.username && (
                <span className="text-danger">Username is required</span>
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
        <div className="card shadow-sm">
          <div className="shadow card-body p-4">
            <div className="flex-column py-4">
              <div className="d-flex justify-content-center">
                <h6>Want to disable your account?</h6>
              </div>
              <div className="d-flex justify-content-center">
                <button
                  onClick={handleClick}
                  className="btn btn-danger rounded-5 text-white shadow"
                >
                  DISABLE
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
