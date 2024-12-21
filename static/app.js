const API_URL = "http://localhost:5000/tasks";

// Load tasks
async function loadTasks() {
  const response = await fetch(API_URL, {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
  });
  const tasks = await response.json();
  const container = document.getElementById("tasksContainer");
  container.innerHTML = "";
  tasks.forEach(task => {
    const div = document.createElement("div");
    div.textContent = `${task.name} - ${task.description || "No description"}`;
    container.appendChild(div);
  });
}

// Add a new task
document.getElementById("taskForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const taskName = document.getElementById("taskName").value;
  const taskDescription = document.getElementById("taskDescription").value;
  await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({ name: taskName, description: taskDescription })
  });
  loadTasks();
});

loadTasks();
