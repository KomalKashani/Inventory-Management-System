    const API = "http://127.0.0.1:9000";

    async function loadItems() {
    const res = await fetch(`${API}/items`);
    const data = await res.json();
    const container = document.getElementById("items");
    container.innerHTML = "";

    data.forEach(item => {
        container.innerHTML += `
        <div class="item-card">
            <h3>${item.name}</h3>
            <div class="count">Count: <b>${item.count}</b></div>

            <div class="actions">
            <button class="inc" onclick="increase('${item.name}')">+</button>
            <button class="dec" onclick="decrease('${item.name}')">-</button>
            <button class="edit" onclick="updateItem('${item.name}', ${item.count})">Edit</button>
            <button class="del" onclick="deleteItem('${item.id}')">Delete</button>

            </div>
        </div>
        `;
    });
    }

    async function addItem() {
    const name = document.getElementById("name").value;
    const count = Number(document.getElementById("count").value);

    if (!name || count < 0) return alert("Invalid input");

    await fetch(`${API}/items`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, count })
    });

    document.getElementById("name").value = "";
    document.getElementById("count").value = "";
    loadItems();
    }

    async function increase(name) {
    const encoded = encodeURIComponent(name);
    await fetch(`${API}/items/${encoded}/increase`, { method: "PATCH" });
    loadItems();
    }

    async function decrease(name) {
    const encoded = encodeURIComponent(name);
    await fetch(`${API}/items/${encoded}/decrease`, { method: "PATCH" });
    loadItems();
    }

    async function deleteItem(id) {
    await fetch(`${API}/items/${id}`, { method: "DELETE" });
    loadItems();
    }


    async function updateItem(oldName, oldCount) {
    const newName = prompt("Update item name:", oldName);
    const newCount = prompt("Update count:", oldCount);

    if (!newName || newCount === null) return;

    await fetch(`${API}/items/${oldName}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
        name: newName,
        count: Number(newCount)
        })
    });

    loadItems();
    }

    loadItems();
