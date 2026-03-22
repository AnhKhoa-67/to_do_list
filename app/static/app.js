const API_BASE = "/api/v1";

// State Management
let currentToken = localStorage.getItem("token");
let currentFilter = "all";

// DOM Elements
const authScreen = document.getElementById("auth-screen");
const dashboard = document.getElementById("dashboard");
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const todoList = document.getElementById("todo-list");
const userEmailSpan = document.getElementById("user-email");
const taskModal = document.getElementById("task-modal");
const taskForm = document.getElementById("task-form");
const viewTitle = document.getElementById("view-title");

// --- Initialization ---
if (currentToken) {
    showDashboard();
}

// --- Auth Functions ---
async function login(email, password) {
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const resp = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            body: formData
        });
        if (!resp.ok) throw new Error("Đăng nhập thất bại");
        const data = await resp.json();
        currentToken = data.access_token;
        localStorage.setItem("token", currentToken);
        localStorage.setItem("email", email);
        showDashboard();
    } catch (err) {
        alert(err.message);
    }
}

async function register(email, password) {
    try {
        const resp = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        if (!resp.ok) throw new Error("Đăng ký thất bại");
        alert("Đăng ký thành công! Vui lòng đăng nhập.");
        document.getElementById("show-login").click();
    } catch (err) {
        alert(err.message);
    }
}

function logout() {
    currentToken = null;
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    dashboard.classList.remove("active");
    authScreen.classList.add("active");
}

function showDashboard() {
    authScreen.classList.remove("active");
    dashboard.classList.add("active");
    userEmailSpan.textContent = localStorage.getItem("email") || "Người dùng";
    fetchTodos();
}

// --- Các hàm cho Todo ---
async function fetchTodos() {
    let url = `${API_BASE}/todos/`;
    if (currentFilter === "today") url = `${API_BASE}/todos/today`;
    else if (currentFilter === "overdue") url = `${API_BASE}/todos/overdue`;

    try {
        const resp = await fetch(url, {
            headers: { "Authorization": `Bearer ${currentToken}` }
        });
        if (resp.status === 401) return logout();
        const data = await resp.json();
        renderTodos(data.items);
    } catch (err) {
        console.error(err);
    }
}

function renderTodos(todos) {
    todoList.innerHTML = "";
    todos.forEach(todo => {
        const card = document.createElement("div");
        card.className = `todo-item glass-card ${todo.is_done ? 'done' : ''}`;
        
        const tagsHtml = todo.tags.map(t => `<span class="tag">${t.name}</span>`).join("");
        const isOverdue = todo.due_date && new Date(todo.due_date) < new Date() && !todo.is_done;
        const dateHtml = todo.due_date ? new Date(todo.due_date).toLocaleString('vi-VN') : "Không có hạn chót";

        card.innerHTML = `
            <div class="todo-header">
                <div class="tag-list">${tagsHtml}</div>
                <div class="todo-actions">
                    <button class="action-btn done-btn" onclick="toggleDone(${todo.id}, ${!todo.is_done})"><i class="fas ${todo.is_done ? 'fa-undo' : 'fa-check'}"></i></button>
                    <button class="action-btn edit-btn" onclick="openEditModal(${JSON.stringify(todo).replace(/"/g, '&quot;')})"><i class="fas fa-edit"></i></button>
                    <button class="action-btn delete-btn" onclick="deleteTodo(${todo.id})"><i class="fas fa-trash"></i></button>
                </div>
            </div>
            <div class="todo-title">${todo.title}</div>
            <div class="todo-desc">${todo.description || ""}</div>
            <div class="todo-footer">
                <span class="todo-due ${isOverdue ? 'overdue' : ''}"><i class="far fa-calendar-alt"></i> ${dateHtml}</span>
            </div>
        `;
        todoList.appendChild(card);
    });
}

async function toggleDone(id, is_done) {
    await fetch(`${API_BASE}/todos/${id}`, {
        method: "PATCH",
        headers: { 
            "Authorization": `Bearer ${currentToken}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ is_done })
    });
    fetchTodos();
}

async function deleteTodo(id) {
    if (!confirm("Bạn có chắc chắn muốn xóa công việc này?")) return;
    await fetch(`${API_BASE}/todos/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${currentToken}` }
    });
    fetchTodos();
}

// --- Lắng nghe sự kiện ---
loginForm.onsubmit = (e) => {
    e.preventDefault();
    login(document.getElementById("login-email").value, document.getElementById("login-password").value);
};

registerForm.onsubmit = (e) => {
    e.preventDefault();
    register(document.getElementById("register-email").value, document.getElementById("register-password").value);
};

document.getElementById("show-register").onclick = () => {
    document.getElementById("auth-forms").style.display = "none";
    document.getElementById("register-forms").style.display = "block";
};

document.getElementById("show-login").onclick = () => {
    document.getElementById("auth-forms").style.display = "block";
    document.getElementById("register-forms").style.display = "none";
};

document.querySelectorAll(".nav-btn[data-filter]").forEach(btn => {
    btn.onclick = () => {
        document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentFilter = btn.dataset.filter;
        viewTitle.textContent = btn.innerText;
        fetchTodos();
    };
});

document.getElementById("logout-btn").onclick = logout;

// --- Logic Modal ---
document.getElementById("add-task-btn").onclick = () => {
    taskForm.reset();
    document.getElementById("task-id").value = "";
    document.getElementById("modal-title").innerText = "Thêm công việc mới";
    taskModal.classList.add("active");
};

document.getElementById("close-modal").onclick = () => taskModal.classList.remove("active");

window.openEditModal = (todo) => {
    document.getElementById("task-id").value = todo.id;
    document.getElementById("task-title").value = todo.title;
    document.getElementById("task-desc").value = todo.description || "";
    if (todo.due_date) {
        const d = new Date(todo.due_date);
        d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
        document.getElementById("task-due").value = d.toISOString().slice(0, 16);
    }
    document.getElementById("task-tags").value = todo.tags.map(t => t.name).join(", ");
    document.getElementById("modal-title").innerText = "Chỉnh sửa công việc";
    taskModal.classList.add("active");
};

taskForm.onsubmit = async (e) => {
    e.preventDefault();
    const id = document.getElementById("task-id").value;
    const data = {
        title: document.getElementById("task-title").value,
        description: document.getElementById("task-desc").value,
        due_date: document.getElementById("task-due").value || null,
        tags: document.getElementById("task-tags").value.split(",").map(t => t.trim()).filter(t => t)
    };

    const method = id ? "PATCH" : "POST";
    const url = id ? `${API_BASE}/todos/${id}` : `${API_BASE}/todos/`;

    await fetch(url, {
        method,
        headers: { 
            "Authorization": `Bearer ${currentToken}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    taskModal.classList.remove("active");
    fetchTodos();
};
