import toast from "react-hot-toast";
const getState = ({ setStore, getActions, getStore }) => {
  return {
    store: {
      user_id: "",
      token: "",
      email: "",
      username: "",
      tasks: [],
    },
    actions: {
      userRegister: ({ username, email, password }, navigate) => {
        const url = "http://localhost:8585/register";
        fetch(url, {
          headers: {
            "Content-Type": "application/json",
          },
          method: "POST",
          body: JSON.stringify({
            username,
            email,
            password,
          }),
        })
          .then((res) => res.json())
          .then((res) => {
            navigate("/login");
            toast.success("Successfully register!");
          })
          .catch((error) => {
            console.log(error);
            toast.error("Server error!");
          });
      },
      userLogin: ({ email, password }, navigate) => {
        const url = "http://localhost:8585/login";
        fetch(url, {
          headers: {
            "Content-Type": "application/json",
          },
          method: "POST",
          body: JSON.stringify({
            email,
            password,
          }),
        })
          .then((res) => {
            if (!res.ok) throw Error(res.status);
            return res.json()
          })
          .then((res) => {
            setStore({
              token: res.token,
              email: res.email,
              user_id: res.user_id,
              username: res.username,
            });
            toast.success("Successful login!");
            getActions().fetchTasks();
            navigate("/");
          })
          .catch((error) => {
            toast.error("Server error.");
            console.log(error);
          });
      },
      setUsername: (data, navigate) => {
        const { user_id, token } = getStore();
        const url = "http://localhost:8585/userlist/";
        const urlToFetch = url + user_id;
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          method: "PUT",
          body: JSON.stringify({
            username: data.username,
          }),
        })
          .then((res) => res.json())
          .then(() => {
            getActions().getUser(navigate)
            toast.success("Username changed successfully!");
          })
          .catch((error) => {
            console.log(error);
            toast.error("Server error!");
          });
      },
      getUser: (navigate) => {
        const { user_id, token } = getStore()
        const url = "http://localhost:8585/user/";
        const urlToFetch = url + user_id
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
        })
          .then((res) => res.json())
          .then((res) => {
            setStore({
              username: res.username
            })
            navigate("/")
          })
          .catch((error) => {
            console.log(error)
          })
      },
      disabledUser: () => {
        const { user_id, token } = getStore();
        const url = "http://localhost:8585/userlist/";
        const urlToFetch = url + user_id;
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          method: "DELETE",
        })
          .then((res) => {
            if (res.ok) {
              toast.success("User disabled successfully.");
              getActions().logout();
            } else {
              toast.error("Server error!");
            }
          })
      },
      logout: () => {
        setStore({
          user_id: "",
          token: "",
          email: "",
          tasks: [],
          username: "",
        });
        toast.success("Logout successfully.");
      },
      fetchTasks: () => {
        const { token } = getStore();
        const url = "http://localhost:8585/tasklist/";
        const { user_id } = getStore();
        const urlToFetch = url + user_id;
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
        })
          .then((res) => {
            if (!res.ok) throw Error(res.status);
            return res.json()
          })
          .then((res) => {
            setStore({
              tasks: res,
            });
          })
          .catch((error) => {
            console.log(error)
            setStore({
              tasks: [],
            })
          });
      },
      newTask: ({ task, description }) => {
        const { token } = getStore();
        const url = "http://localhost:8585/tasks";
        const { user_id } = getStore();
        fetch(url, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          method: "POST",
          body: JSON.stringify({
            user_id,
            task,
            description,
          }),
        })
          .then((res) => res.json())
          .then(() => {
            toast.success("Successfully created!");
            getActions().fetchTasks();
          })
          .catch((error) => {
            console.log(error);
            toast.error("Server error.");
          });
      },
      deleteTask: (id) => {
        const { token } = getStore();
        const url = "http://localhost:8585/task/";
        const urlToFetch = url + id;
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          method: "DELETE",
        })
          .then((res) => {
            if (res.ok) {
              toast.success("Task delete successfully.");
              getActions().fetchTasks();
            } else {
              toast.error("Server error!");
            }
          })
          .catch((error) => {
            console.log(error);
            alert("Error in the server.");
          });
      },
      updateTask: ({ task, description }, id) => {
        const { token, user_id } = getStore();
        console.log(user_id);
        const urlToFetch = `http://localhost:8585/task/${id}`;
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          method: "PUT",
          body: JSON.stringify({
            id,
            task,
            description,
            is_completed: false,
            user_id
          }),
        })
          .then((res) => res.json())
          .then(() => {
            toast.success("Task updated successfully.");
            getActions().fetchTasks();
          })
          .catch((error) => {
            console.log(error);
            toast.error("Server error.");
          });
      },
      setCompleted: (id) => {
        const { token } = getStore();
        const url = "http://localhost:8585/task/";
        const urlToFetch = url + id;
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          method: "PUT",
          body: JSON.stringify({
            is_completed: true,
          }),
        })
          .then((res) => res.json())
          .then(() => {
            getActions().fetchTasks();
            toast.success("Task marked as completed!");
          })
          .catch((error) => {
            console.log(error);
            toast.error("Server error.");
          });
      },
      setIncomplete: (id) => {
        const { token } = getStore();
        const url = "http://localhost:8585/task/";
        const urlToFetch = url + id;
        fetch(urlToFetch, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
          method: "PUT",
          body: JSON.stringify({
            is_completed: false,
          }),
        })
          .then((res) => res.json())
          .then(() => {
            getActions().fetchTasks();
            toast.error("Task marked as incomplete!");
          })
          .catch((error) => {
            console.log(error);
            toast.error("Server error.");
          });
      },
    },
  };
};
export default getState;
