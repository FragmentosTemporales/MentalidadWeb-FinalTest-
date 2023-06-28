import NewTask from "../component/_newTask";
import TasksList from "../component/_tasksList";
import { useContext } from "react";
import { Context } from "../store/Context";
import CompletedTasksList from "../component/_completedTasks";

function Home() {
  const { store, actions } = useContext(Context);
  const { username } = store;
  return (
    <main className="body container-fluid">
      <div className="d-flex justify-content-center pt-2">
        <h5 className="text-white">
          Hi {username}!
        </h5>
      </div>
      <div className="row">
        <div 
        className="col-md-5 flex-column">
          <div className="" style={{ maxHeight: "300px" }}>
            <NewTask />
          </div>
          <div 
          className="">
            <CompletedTasksList />
          </div>
        </div>
        <div className="col-md-7">
          <TasksList />
        </div>
      </div>
    </main>
  );
}

export default Home;
